import os
import numpy
import urllib2
import random
import math
import csv

from common_private import *

#GSV_KEY = ""

HTML_SOURCE_FOLDER = "./html_source"

YEAR = 2012
MONTHS = ['jan', 'feb', 'mar', 'apr', 'may', 'jun', 'jul', 'aug', 'sep', 'oct', 'nov', 'dec']
SSO_PATH = 'sso'
POLICE_PATH = 'crimes'
ROAD_PATH = 'roads'
CSV_PATH = 'csv'
DETECTION_PATH = 'detection'
# baseURI = 'https://data.police.uk/api/crimes-street/all-crime?'

CATEGORY_URI = 'https://data.police.uk/api/crime-categories?date='
CRIME_URI = 'https://data.police.uk/api/crimes-street/all-crime?'
STOP_AND_SEARCH_URI = 'https://data.police.uk/api/stops-street?'
OVERPASSURI = 'http://overpass-api.de/api/map?bbox=%f,%f,%f,%f'
OSMDATAFOLDER = 'osmdata'
DATA_FOLDER = 'data'
STREETVIEW_IMAGES_FOLDER = 'streetviewimages'
KMLFOLDER = 'kml'
KMLROADFOLDER = 'kmlroads'

# https://en.wikipedia.org/wiki/Latitude
ONE_KM_IN_DEGREES_LAT = 1/111.132 # at 45 \phi
# https://en.wikipedia.org/wiki/Longitude
ONE_KM_IN_DEGREES_LON = 1/78.847 # at 45 \phi

FAKE_OSM_FILE = "fake.osm"

EARTH_RADIUS = 6378137.0
POLY_DISTANCE = 800.0

UK_BOUNDS = [[49.545286, -12.679143], [62.708215, -12.679143], [62.708215, 1.807802], [49.545286, 1.807802]]

US_BOUNDS = [[25.549145, -124.488393], [48.658102, -124.488393], [48.658102, -59.647340], [25.549145, -59.647340]] # No Alaska!

UK_ZONES = [
    [[50.813877, -1.967289], [52.740575, 0.279415]],
    [[51.784125, -4.029522], [53.286836, -1.392639]],
    [[53.195716, -2.638410], [54.558298, -1.011987]],
    [[54.272359, -3.323585], [55.341276, -1.627951]],
    [[54.925851, -4.880799], [56.024081, -2.790671]],
    [[56.347606, -4.894641], [57.699786, -2.029367]]
    ]

US_ZONES = [
    [[30.524619, -94.120073], [41.323363, -81.357743]],
    [[34.842799, -80.794360], [36.560202, -76.891627]]
]

MULTIPLIER = 1000000
FAKE_REQUESTS_COUNT = 9

CSV_CRIME_FIELDNAMES = ['family_id', 'data_type',
                  'category', 'persistent_id', 'month',
                  'location_latitude', 'location_longitude', 'location_street_id', 'location_street_name',
                  'context', 'id', 'location_type', 'location_subtype',
                  'outcome_status_category', 'outcome_status_date', 'on_family_road'
                  ]

CSV_STOPANDSEARCH_FIELDNAMES = [ 'family_id', 'data_type',
    'type', 'involved_person', 'datetime', 'operation', 'operation_name',
    'location_latitude', 'location_longitude', 'location_street_id', 'location_street_name',
    'gender', 'age_range', 'self_defined_ethnicity', 'officer_defined_ethnicity', 'legislation', 'object_of_search',
    'outcome', 'outcome_linked_to_object_of_search', 'removal_of_more_than_outer_clothing', 'on_family_road'
]

CSV_CLOSEST_POI_FIELDNAMES = [ 'family_id', 'latitude', 'longitude', 'poi_classification',
                               'poi_category', 'count', 'distance', 'average_distance', 'points', 'tags']


CSV_URBANICITY_VARIABLES = ['park', 'pitch', 'playground', 'dog_park', 'garden', 'golf_course', 'recreation_ground', 'village_green', 'forest', 'farmland', 'grass', 'meadow']

CSV_URBANICITY_POI_FIELDNAMES = ['familyid', 'density', 'PerGreen', 'numGreen', 'SCIIurban3', 'PopDensity']

# OSM_POI_CATEGORIES = {
#     "Leisure" : ["park", "pitch ", "playground ", "sports_centre", "swimming_pool", "swimming_area", "water_park", "track", "bandstand", "dog_park", "garden", "golf_course"],
#     "Amenity" : ["bar", "bbq", "cafe", "drinking_water", "fast_food", "food_court", "ice_cream", "pub", "restaurant", "college", "kindergarten", "library ", "school ", "university ", "clinic ", "dentist ", "doctors", "hospital ", "pharmacy ", "social_facility ", "casino", "community_centre", "social_centre", "nightclub", "marketplace ", "gym", "place_of_worship", "police"],
#     "Public Transportation": ["station", "platform", "stop_position", "stop_area"],
#     "Land Use": ["recreation_ground", "village_green", "residential ", "forest", "farmland", "grass", "meadow", "industrial"]
# }

# SUPPORT FUNCTIONS #
def merge_two_dicts(x, y):
    '''Given two dicts, merge them into a new dict as a shallow copy.'''
    z = x.copy()
    z.update(y)
    return z

def getRandomLocations(lat, lon, count):
    if count == 0:
        print 'No fake locations to determine'
        return []
    in_uk = point_inside_polygon(lat, lon, UK_BOUNDS)
    print 'Determining %i fake locations for (%f, %f) inside %s' % (count, lat, lon, 'UK' if in_uk else 'US')
    result = []
    random.seed()
    for i in range(0, count):
        zone_pool = US_ZONES
        if in_uk:
            zone_pool = UK_ZONES
        rnd = random.randint(0, len(zone_pool) - 1)
        zone = zone_pool[rnd]
        min = zone[0]
        max = zone[1]
        rlat = random.randint(int(min[0] * MULTIPLIER), int(max[0] * MULTIPLIER))
        rlon = random.randint(int(min[1] * MULTIPLIER), int(max[1] * MULTIPLIER))
        #print 'Random:', [float(rlat)/float(MULTIPLIER), float(rlon)/float(MULTIPLIER)]
        result.append([float(rlat)/float(MULTIPLIER), float(rlon)/float(MULTIPLIER)])
    return result

# determine if a point is inside a given polygon or not
# Polygon is a list of (x,y) pairs.
def point_inside_polygon(x, y, poly):
    n = len(poly)
    inside = False
    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        #print p1x, ',', p1y, ' - ', p2x, ',', p2y
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xinters = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xinters:
                        inside = not inside
        p1x,p1y = p2x,p2y
    return inside

# Determine if a point is on any of the given segments
def point_on_segments(x, y, points):
    #print 'point_on_segments', [x,y], points
    n = len(points)
    point1 = points[0]
    for i in range(1, n):
        #print 'range', i
        point2 = points[i]
        distance = determineRadiusSegmentDistance(x, y, [point1, point2])
        #print 'Distance point to line', distance, point1, point2, [x,y]
        if distance <= 10.0:
            return True
        point1 = point2
    return False


def printHeadline(data):
    print '########################################'
    print data
    print '########################################'

def determineRadiusDistance(lat, lon, latp, lonp):
    radius = 6371e3
    phi1 = math.radians(lat)
    lambda1 = math.radians(lon)
    phi2 = math.radians(latp)
    lambda2 = math.radians(lonp)

    delta_phi = phi2 - phi1
    delta_lambda = lambda2 - lambda1
    a = math.sin(delta_phi/2) * math.sin(delta_phi/2) + math.cos(phi1) * math.cos(phi2) * math.sin(delta_lambda/2) * math.sin(delta_lambda/2)
    c = 2 * math.atan2(math.sqrt(a), math.sqrt(1-a))
    d = radius * c
    return d

def determineRadiusSegmentDistance(lat, lon, segment):
    latp,lonp = determinePointOnSegment(lat, lon, segment)

    return determineRadiusDistance(lat, lon, latp, lonp)


def determineDistance(vect1, vect2, vectP):
    vectN = vect2 - vect1
    vectPA = vect1 - vectP
    c = numpy.dot(vectN, vectPA)
    if c > 0.0:
        return numpy.dot(vectPA, vectPA)
    vectBP = vectP - vect2
    if numpy.dot(vectN, vectBP) > 0.0:
        return numpy.dot(vectBP, vectBP)
    # print vectN, ": ", numpy.dot(vectN, vectN)
    vectE = vectPA - vectN * (c / numpy.dot(vectN, vectN))
    return numpy.dot(vectE, vectE)


def determinePointOnSegment(lat, lon, segment):
    sx1 = segment[0][0]
    sy1 = segment[0][1]
    sx2 = segment[1][0]
    sy2 = segment[1][1]
    px = lat
    py = lon
    xDelta = sx2 - sx1
    yDelta = sy2 - sy1
    if xDelta == 0.0 and yDelta == 0.0:
        return [lat, lon]
    u = ((px - sx1) * xDelta + (py - sy1) * yDelta) / (xDelta * xDelta + yDelta * yDelta)
    if u < 0:
        return [sx1, sy1]
    elif u > 1:
        return [sx2, sy2]
    else:
        return [(sx1 + u * xDelta), (sy1 + u * yDelta)]

def determineDirection(p1, p2):
    deltaX = p1[0] - p2[0]
    deltaY = p1[1] - p2[1]
    angleInDegrees = math.atan2(deltaY, deltaX) * 180 / math.pi
    while angleInDegrees < 0.0:
        angleInDegrees += 360.0
    while angleInDegrees >= 360.0:
        angleInDegrees -= 360.0
    return angleInDegrees


def checkOsmExists(filename, lat, lon, osm_output_folder):
    if not os.path.exists(osm_output_folder):
        return False
    if not filename is None:
        filepath = os.path.join(osm_output_folder, str(filename) + '.osm')
        if os.path.isfile(filepath):
            print 'File already exists: %s' % (filepath)
            return True
    return False

def downloadOsm(filename, lat, lon, osm_output_folder):
    if not os.path.exists(osm_output_folder):
        os.makedirs(osm_output_folder)
    if not filename is None:
        filepath = os.path.join(osm_output_folder, filename)
        if os.path.isfile(filepath):
            print 'File already exists: %s' % (filepath)
            return
    else:
        filepath = os.path.join(osm_output_folder, FAKE_OSM_FILE)
    minlat = lat - ONE_KM_IN_DEGREES_LAT
    minlon = lon - ONE_KM_IN_DEGREES_LON
    maxlat = lat + ONE_KM_IN_DEGREES_LAT
    maxlon = lon + ONE_KM_IN_DEGREES_LON
    url = OVERPASSURI % (minlon, minlat, maxlon, maxlat)
    retry = True
    while retry:
        try:
            socket = urllib2.urlopen(url)
        except urllib2.HTTPError as e:
            print 'The server couldn\'t fulfill the request. Error code: ', e.code
        except urllib2.URLError as e:
            print 'We failed to reach a server. Reason: ', e.reason
        else:
            f = open(filepath, 'wb')
            block_sz = 8192
            while True:
                buffer = socket.read(block_sz)
                if not buffer:
                    break
                f.write(buffer)
            f.close()
            retry = False


def readOsm(filename, osm_output_folder):
    if not os.path.exists(osm_output_folder):
        os.makedirs(osm_output_folder)
    filepath = os.path.join(osm_output_folder, filename)
    f = open(filepath, 'r')
    data = f.read()
    f.close()
    return data


def determinePolygon(lat, lon):
    poly = []
    latR = math.radians(lat)
    lonR = math.radians(lon)
    d = POLY_DISTANCE / EARTH_RADIUS
    #axisX = [latR]
    #axisY = [lonR]
    for i in range(0, 360):
        tc = math.radians(i)
        latX = math.asin( (math.sin(latR) * math.cos(d)) + (math.cos(latR) * math.sin(d) * math.cos(tc)) )
        lonX = lonR
        if math.cos(latX) != 0.0:
            lonX = ((lonR - math.asin( math.sin(tc) * math.sin(d) / math.cos(latR)) + math.pi) % (2 * math.pi)) - math.pi
        #tc = math.radians(i)
        #latPoint = math.asin((math.sin(latR) * math.cos(d)) + (math.cos(latR) * math.sin(d) * math.cos(tc)))
        #lonPoint = lonR
        #if math.cos(latPoint) != 0.0:
        #    lonPoint = ((lonR - math.asin( math.sin(tc) * math.sin(d) / math.cos(latR)) + math.pi) % (2 * math.pi)) - math.pi
        point = [math.degrees(latX), math.degrees(lonX)]
        poly.append(point)
        #axisX.append(latX)
        #axisY.append(lonX)
    #print poly
    #plt.plot(axisX, axisY, 'ro')
    #plt.show()
    return poly


def initCSV(filepath, headers):
    with open(filepath, 'wb') as csvfile:
        try:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            writer.writeheader()
        except csv.Error as e:
            print '# Error while writing headers in common.initCSV', e
            print '# Data:', headers
        except UnicodeEncodeError as e:
            print '# Error while writing headers in common.initCSV', e
            print '# Data:', headers

def appendCSV(data, filepath, headers):
    with open(filepath, 'ab') as csvfile:
        try:
            writer = csv.DictWriter(csvfile, fieldnames=headers)
            if isinstance(data, dict):
                writer.writerow(data)
            else:
                writer.writerows(data)
        except csv.Error as e:
            print '# Error while writing rows in common.appendCSV', e
            print '# Filepath:', filepath
            print '# Data:', data
        except UnicodeEncodeError as e:
            print '# Error while writing rows in common.appendCSV', e
            print '# Filepath:', filepath
            print '# Data:', data

if __name__ == '__main__':
    # common.py executed as script
    # do something
    print "Not this way"