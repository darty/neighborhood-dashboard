from osm_common import *
from common import *
from geopy.distance import vincenty

WANTED_HIGHWAY_TAGS = [
    'motorway', 'trunk', 'primary', 'secondary', 'tertiary', 'unclassified', 'residential', 'service',
    'motorway_link', 'trunk_link', 'primary_link', 'secondary_link', 'tertiary_link',
    'living_street', 'pedestrian', 'track',
    'road', 'construction'
]

def calculateDistance(p1, p2):
    #print "Reversed", p1, p2
    distance = vincenty(reversed(p1), reversed(p2)).meters
    #print p1[::-1], p2[::-1], distance
    return distance

def calculateLength(points):
    if len(points) <= 1:
        return 0
    result = 0
    p1 = points[0]
    for i in range(1, len(points)):
        p2 = points[i]
        result += calculateDistance(p1, p2)
        p1 = p2
    return result

def calculateSegmentLengths(segments):
    result = 0.0
    for segment in segments:
        result+= calculateDistance(segment[0], segment[1])
    # result = 0
    # s1 = segments[0]
    # #for segment in segments:
    # for i in range(1, len(segments)):
    #     s2 = segments[i]
    #     result += calculateDistance(s1, s2)
    #     s1 = s2
    return result

MAX_LENGTH = 200.0 # meters

def calculateCloserPoint(p1, p2, percentage):
    #print p1, p2, percentage
    pointx = p1[0] + (p2[0] - p1[0]) * percentage
    pointy = p1[1] + (p2[1] - p1[1]) * percentage
    result = [pointx, pointy]
    return result

def isclose(a, b, rel_tol=1e-09, abs_tol=0.0):
    return abs(a-b) <= max(rel_tol * max(abs(a), abs(b)), abs_tol)

def shortenSegment(points, middle_point, length_over, length_left, length_right, max_length):
    # if length_left == length_right:
    if isclose(length_left, length_right):
        # shorten both with length_over / 2
        point_left = calculateCloserPoint(middle_point, points[0], ((max_length/2)) / length_left)
        point_right = calculateCloserPoint(middle_point, points[1], ((max_length/2)) / length_right)
        print "Both", [point_left, point_right]
        return [point_left, point_right]
    elif length_left > length_right:
        # shorten left with length_left - length_right
        noemer = (length_left - length_over)
        # noemer = length_right
        # if length_right > length_left:
        #     noemer = (max_length - length_right)
        point_left = calculateCloserPoint(middle_point, points[0], noemer / length_left)
        print "Left", [point_left, points[1]]
        return [point_left, points[1]]
    else: #  length_left < length_right:
        # shorten_right with length_right - length_left
        noemer = (length_right - length_over)
        # noemer = length_left
        # if length_left > length_right:
        #     noemer = (max_length - length_left)
        point_right = calculateCloserPoint(middle_point, points[1], noemer / length_right)
        print "Right", [points[0], point_right]
        return [points[0], point_right]

def minimizeRoads(points, segment_part, segment_point):
    # filter out identical points
    filtered_list = []

    for point in points:
        if not point in filtered_list:
            filtered_list.append(point)
        else:
            print "Filtered out double location"

    points = filtered_list


    current_length = calculateLength(points)
    if current_length > MAX_LENGTH:
        print "Recalculating road, old length", current_length
    while current_length > MAX_LENGTH:
        over_middle = False
        left = []
        right = []
        point1 = points[0]
        i = 1
        if len(points) < 3:
            left = [[points[0], segment_point]]
            right = [[segment_point, points[1]]]
        else:
            while i < len(points):
                point2 = points[i]
                current_segment = [point1, point2]
                if not over_middle:
                    if current_segment != segment_part:
                        #print "Left ", current_segment
                        left.append(current_segment)
                    else:
                        #print "Left ", [point1, segment_point]
                        left.append([point1, segment_point])
                        #print "Right ", [segment_point, point2]
                        right.append([segment_point, point2])
                        over_middle = True
                else:
                    #print "Right ", current_segment
                    right.append(current_segment)
                point1 = point2
                i += 1

        print "Segments", left, right
        length_left = calculateSegmentLengths(left)
        length_right = calculateSegmentLengths(right)

        print "Lengths", length_left, length_right, current_length

        length_over = current_length - MAX_LENGTH
        if len(points) > 2:
            if length_left > length_right:
                length_left_segment = calculateDistance(points[0], points[1])
                if length_left_segment > length_over:
                    # shorten one segment
                    print "Shortening left segment", length_left_segment, length_over, (length_left_segment - length_over) / length_left_segment
                    points[0] = calculateCloserPoint(points[1], points[0], (length_left_segment - length_over) / length_left_segment)
                else:
                    points = points[1:]
            else:
                length_right_segment = calculateDistance(points[-2], points[-1])
                if length_right_segment > length_over:
                    # shorten one segment
                    print "Shortening right segment", length_right_segment, length_over, (length_right_segment - length_over) / length_right_segment
                    points[-1] = calculateCloserPoint(points[-2], points[-1], (length_right_segment - length_over) / length_right_segment)
                else:
                    points = points[:-1]
        else:
            points = shortenSegment(points, segment_point, length_over, length_left, length_right, MAX_LENGTH)
        print "New points", points
        current_length = calculateLength(points)
        if isclose(current_length, MAX_LENGTH):
            break

    print "New length", current_length
    return points


def retrieveClosestRoad(roads, lat, lon):
    shortestDistance = -1
    closestRoad = -1
    vectA = numpy.array([lat, lon])
    shortestSegment = []
    for rid in roads:
        tags = dict(roads[rid]["tags"])
        if not 'highway' in tags.keys() or not tags['highway'] in WANTED_HIGHWAY_TAGS:
            continue
        points = roads[rid]["points"]
        point1 = points[0]
        for point in points[1::]:
            point2 = point
            if point1 == point2:
                print 'Points on road are identical'
                continue
            vect1 = numpy.array(point1)
            vect2 = numpy.array(point2)
            distance = determineDistance(vect1, vect2, vectA)
            if shortestDistance == -1 or shortestDistance > distance:
                shortestDistance = distance
                closestRoad = rid
                shortestSegment = [point1, point2]
            point1 = point2
    if closestRoad == -1:
        return {}
    #
    # # shortestDistance
    # # shortestSegment
    # closest_road = roads[closestRoad]
    # closest_road_points = closest_road['points']
    # segment_point = [lat, lon]
    # if shortestDistance != 0.0:
    #     segment_point = determinePointOnSegment(lat, lon, shortestSegment)
    #
    # before = []
    # after = []
    # passed = False
    # point1 = closest_road_points[0]
    # total_length = 0.0
    # length_before = 0.0
    # length_after = 0.0
    # for point in closest_road_points[1::]:
    #     point2 = point
    #     current_length = vincenty(point1, point2).meters
    #     if shortestSegment == [point1, point2]:
    #         before.append([point1, segment_point])
    #         after.append([segment_point, point2])
    #         length_before += vincenty(point1, segment_point).meters
    #         length_after += vincenty(segment_point, point2).meters
    #         passed = True
    #     else:
    #         if not passed:
    #             before.append([point1, point2])
    #             length_before += current_length
    #         else:
    #             after.append([point1, point2])
    #             length_after += current_length
    #     total_length += current_length
    #
    # while total_length > 200.0:
    #     if length_before > length_after:
    #         shorten_part(before.reverse(), 200.0 - length_after)
    #         before.reverse()
    #     else:
    #         shorten_part(after, 200.0 - length_before)
    #     calculateLength(before, length_before)
    #     calculateLength(after, length_after)
    #     total_length = length_before + length_after

    result = roads[closestRoad]
    segment = { 'distance': shortestDistance, 'points': shortestSegment }
    if shortestDistance == 0.0:
        segment['segment-point'] = [lat, lon]
    else:
        segment['segment-point'] = determinePointOnSegment(lat, lon, shortestSegment)
    result['segment'] = segment
    result['points'] = minimizeRoads(result['points'], shortestSegment, segment['segment-point'])
    return result

def retrievePointOnRoad(roads, point):
    shortestSegment = []
    vectA = numpy.array(point)
    point1 = roads[0]
    shortestDistance = -1
    for point in roads[1::]:
        point2 = point
        if point1 == point2:
            print 'Points on road are identical'
            continue
        vect1 = numpy.array(point1)
        vect2 = numpy.array(point2)
        distance = determineDistance(vect1, vect2, vectA)
        if shortestDistance == -1 or shortestDistance > distance:
            shortestDistance = distance
            shortestSegment = [point1, point2]
        point1 = point2
    if shortestDistance == 0.0:
        return point
    else:
        return determinePointOnSegment(vectA[0], vectA[1], shortestSegment)

def writeRoadKmlPoints(familyid, road_data, output_folder):
    if not os.path.exists(output_folder):
        os.makedirs(output_folder)
    filepath = os.path.join(output_folder, str(familyid) + '.kml')
    f = open(filepath, 'w')
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
    f.write("<Document>\n")
    f.write("\t<name>" + filepath +"</name>\n")
    i = 0
    points = []
    if 'roads' in road_data and 'points' in road_data['roads']:
        points = road_data['roads']['points']
    for point in points:
        f.write("\t<Placemark>\n")
        f.write("\t\t<name>" + str(i) + "</name>\n")
        f.write("\t\t<Point>\n")
        f.write("\t\t\t<coordinates>" + str(point[1]) + "," + str(point[0]) + ",0.0 </coordinates>\n")
        f.write("\t\t</Point>\n")
        f.write("\t</Placemark>\n")
        i += 1
    f.write("</Document>\n")
    f.write("</kml>\n")
    f.close()

def writeFamilyKmlPoints(familyid, point_data, kml_output_folder):
    if not os.path.exists(kml_output_folder):
        os.makedirs(kml_output_folder)
    filepath = os.path.join(kml_output_folder, str(familyid) + '.kml')
    f = open(filepath, 'w')
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
    f.write("<Document>\n")
    f.write("\t<name>" + filepath +"</name>\n")
    i = 0
    for point,headings in point_data:
        # point = data[0]
        # headings = data[1]
        f.write("\t<Placemark>\n")
        f.write("\t\t<name>" + str(i) + "</name>\n")
        f.write("\t\t<Point>\n")
        f.write("\t\t\t<coordinates>" + str(point[1]) + "," + str(point[0]) + ",0.0 </coordinates>\n")
        f.write("\t\t</Point>\n")
        f.write("\t\t<ExtendedData>\n")
        f.write("\t\t\t<Data name=\"headings\">\n")
        f.write("\t\t\t<value>" + str(headings[0]) + "," + str(headings[1]) + "</value>\n")
        f.write("\t\t\t</Data>\n")
        f.write("\t\t</ExtendedData>\n")
        f.write("\t</Placemark>\n")
        i += 1
    f.write("</Document>\n")
    f.write("</kml>\n")
    f.close()

def determineRoadPoints(family, road_data):
    points = road_data['roads']['points']
    segment = road_data['roads']['segment']
    startPoint = points[0]
    endPoint = points[len(points) - 1]
    midPoint = segment['segment-point']
    p1 = [startPoint[0] - ((startPoint[0] - midPoint[0]) / 2), startPoint[1] - ((startPoint[1] - midPoint[1]) / 2)]
    p2 = [midPoint[0] - ((midPoint[0] - endPoint[0]) / 2), midPoint[1] - ((midPoint[1] - endPoint[1]) / 2)]
    r1 = retrievePointOnRoad(points, p1)
    r2 = retrievePointOnRoad(points, p2)
    family_point_data = [
        [startPoint, [determineDirection(startPoint, r1), determineDirection(r1, startPoint)]],
        [r1, [determineDirection(r1, midPoint), determineDirection(r1, startPoint)]],
        [midPoint, [determineDirection(midPoint, r2), determineDirection(midPoint, r1)]],
        [r2, [determineDirection(r2, endPoint), determineDirection(r2, midPoint)]],
        [endPoint, [determineDirection(r2, endPoint), determineDirection(endPoint, r2)]],
    ]
    return family_point_data

# def writeRoadPoints(family, road_data):
#     family_point_data = determineRoadPoints(family, road_data)
#     writeFamilyKmlPoints(family, family_point_data)

def retrieveFamilyRoads(family, lat, lon, random_locations, osm_output_folder):
    # If already downloaded OSM data, just parse that and continue
    if not checkOsmExists(family, lat, lon, osm_output_folder):
        random.seed()
        family_done = False
        active = True
        while active:
            rnd = random.randint(0, FAKE_REQUESTS_COUNT)
            if rnd > 0 and len(random_locations) > 0:
                # rnd location
                fake_location = random_locations.pop(random.randint(0, len(random_locations) - 1))
                print 'Fake OSM request %s' % (fake_location)
                downloadOsm(None, fake_location[0], fake_location[1], osm_output_folder)
            elif not family_done:
                print 'Real OSM request %s, %s' % (lat, lon)
                downloadOsm(str(family) + '.osm', lat, lon, osm_output_folder)
                family_done = True
            if family_done and len(random_locations) == 0:
                active = False
    result = {}
    polygon = determinePolygon(lat, lon)
    data = readOsm(str(family) + '.osm', osm_output_folder)
    roads = parseOsm(data)
    result['roads'] = retrieveClosestRoad(roads, lat, lon)
    result['pois'] = parsePois(data, polygon)
    result['closest_pois'] = processPoisDistances(result['pois'], lat, lon)
    return result

# def retrieveFamilyRoads(family, lat, lon, random_locations, osm_output_folder):
#     result = {}
#     # If already downloaded OSM data, just parse that and continue
#     if checkOsmExists(family, lat, lon, osm_output_folder):
#         polygon = determinePolygon(lat, lon)
#         data = readOsm(str(family) + '.osm', osm_output_folder)
#         roads = parseOsm(data)
#         result['roads'] = retrieveClosestRoad(roads, lat, lon)
#         result['pois'] = parsePois(data, polygon)
#         result['closest_pois'] = processPoisDistances(result['pois'], lat, lon)
#         return result
#     # Else start the random/real OSM download sequence
#     random.seed()
#     family_done = False
#     active = True
#     while active:
#         rnd = random.randint(0, FAKE_REQUESTS_COUNT)
#         if rnd > 0 and len(random_locations) > 0:
#             # rnd location
#             fake_location = random_locations.pop(random.randint(0, len(random_locations) - 1))
#             print 'Fake OSM request %s' % (fake_location)
#             downloadOsm(None, fake_location[0], fake_location[1], osm_output_folder)
#         elif not family_done:
#             # actual location
#             result['roads'] = {}
#             result['pois'] = {}
#             polygon = determinePolygon(lat, lon)
#             print 'Processing Roads for %s at location (%s,%s)'% (family, lat, lon)
#             downloadOsm(str(family) + '.osm', lat, lon, osm_output_folder)
#             data = readOsm(str(family) + '.osm', osm_output_folder)
#             roads = parseOsm(data)
#             result['roads'] = retrieveClosestRoad(roads, lat, lon)
#             result['pois'] = parsePois(data, polygon)
#             result['closest_pois'] = processPoisDistances(result['pois'], lat, lon)
#             family_done = True
#         if family_done and len(random_locations) == 0:
#             active = False
#     return result

def writeClosestPoiHeadersToCsv(csvfolder, poi_filename):
    if not os.path.exists(csvfolder):
        os.makedirs(csvfolder)
    initCSV(os.path.join(csvfolder, poi_filename), CSV_CLOSEST_POI_FIELDNAMES)

def writeClosestPoiToCsv(family, lat, lon, data, csvfolder, poi_filename):
    if not os.path.exists(csvfolder):
        os.makedirs(csvfolder)
    csv_data = []
    for classification in data:
        for poi_type in data[classification]:
            poi_data = data[classification][poi_type]
            str_points = ''
            for point in poi_data['points']:
                str_points += '('
                str_points += str(point[0])
                str_points += ';'
                str_points += str(point[1])
                str_points += ')-'
            str_tags = ''
            for tag in poi_data['tags']:
                str_tags += tag
                str_tags += ':'
                str_tags += poi_data['tags'][tag]
                str_tags += ';'
            poi_csv_data = {'family_id': family,
                   'latitude': lat,
                   'longitude': lon,
                   'poi_classification': classification,
                   'poi_category': poi_type.encode("utf8"),
                   'count': poi_data['count'],
                   'distance': poi_data['distance'],
                   'average_distance': poi_data['average_distance'],
                   'points': str_points[:-1],
                   'tags': str_tags[:-1].encode("utf8")
                   }
            csv_data.append(poi_csv_data)
    appendCSV(csv_data, os.path.join(csvfolder, poi_filename), CSV_CLOSEST_POI_FIELDNAMES)