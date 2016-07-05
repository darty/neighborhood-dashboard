import xml.dom.minidom

from common import *


def domParseNode(elem):
    result = dict(id=int(elem.attributes["id"].value),
                  lat=float(elem.attributes["lat"].value),
                  lon=float(elem.attributes["lon"].value))
    tags = {}
    for subelem in elem.childNodes:
        if subelem.nodeName == "tag":
            k = subelem.attributes["k"].value
            v = subelem.attributes["v"].value
            tags[k] = v
    result['tags'] = tags
    return result
    # for key in elem.attributes.keys():
    #     print key, ":", elem.attributes[key].value


def domParseWay(elem):
    result = {'id': int(elem.attributes["id"].value)}
    nds = []
    tags = {}
    for subelem in elem.childNodes:
        if subelem.nodeName == "nd":
            nds.append(int(subelem.attributes["ref"].value))
        elif subelem.nodeName == "tag":
            k = subelem.attributes["k"].value
            v = subelem.attributes["v"].value
            tags[k] = v
    result["nds"] = nds
    result["tags"] = tags
    return result
    # for key in elem.attributes.keys():
    #     print key, ":", elem.attributes[key].value


def domParseRelation(elem):
    for key in elem.attributes.keys():
        print key, ":", elem.attributes[key].value


def parseOsm(dataString):
    nodes = {}
    ways = {}
    # relations = {}
    data = xml.dom.minidom.parseString(dataString)
    data = data.getElementsByTagName("osm")[0]

    for elem in data.childNodes:
        if elem.nodeName == "node":
            id = int(elem.attributes["id"].value)
            nodes[id] = domParseNode(elem)
        elif elem.nodeName == "way":
            id = int(elem.attributes["id"].value)
            ways[id] = domParseWay(elem)
            # elif elem.nodeName == "relation":
            #     id = elem.attributes["id"].value
            #     relations[id] = DomParseRelation(elem)
    result = {}
    for key in ways:
        points = []
        nds = ways[key]["nds"]
        for nid in nds:
            # print nid
            # print nodes[nid]
            lat = nodes[nid]["lat"]
            lon = nodes[nid]["lon"]
            points.append([lat, lon])
        result[key] = {'points': points, 'tags': ways[key]["tags"]}
    return result


classifications = ['amenity', 'leisure', 'public_transport', 'landuse', 'place']


def parsePois(dataString, polygon):
    nodes = {}
    ways = {}
    # relations = {}
    data = xml.dom.minidom.parseString(dataString)
    data = data.getElementsByTagName("osm")[0]

    for elem in data.childNodes:
        if elem.nodeName == "node":
            id = int(elem.attributes["id"].value)
            nodes[id] = domParseNode(elem)
        elif elem.nodeName == "way":
            id = int(elem.attributes["id"].value)
            ways[id] = domParseWay(elem)
            # elif elem.nodeName == "relation":
            #     id = elem.attributes["id"].value
            #     relations[id] = DomParseRelation(elem)

    result = {}
    for key in ways:
        if ways[key]['tags']:
            nds = ways[key]["nds"]
            for classification in classifications:
                if classification in ways[key]['tags']:
                    measure = ways[key]['tags'][classification]

                    points = []

                    # Check inside
                    inside = False
                    for nid in nds:
                        lat = nodes[nid]["lat"]
                        lon = nodes[nid]["lon"]
                        if point_inside_polygon(float(lat), float(lon), polygon):
                            inside = True
                        points.append([lat, lon])
                    if not inside:
                        continue

                    if not classification in result:
                        result[classification] = {}
                    if not measure in result[classification]:
                        result[classification][measure] = []
                    result[classification][measure].append({'points': points, 'tags': ways[key]['tags']})

    for key in nodes:
        if nodes[key]['tags']:
            lat = nodes[key]["lat"]
            lon = nodes[key]["lon"]
            if not point_inside_polygon(float(lat), float(lon), polygon):
                continue
            points = [[lat, lon]]

            for classification in classifications:
                if classification in nodes[key]['tags']:
                    measure = nodes[key]['tags'][classification]
                    if not classification in result:
                        result[classification] = {}
                    if not measure in result[classification]:
                        result[classification][measure] = []
                    result[classification][measure].append({'points': points, 'tags': nodes[key]['tags']})
    return result


def processPoisDistances(data, lat, lon):
    result = {}
    for classification in data:
        result[classification] = {}
        for poi_type in data[classification]:
            shortest_distance = None
            shortest_data = None
            distances = []
            pois = data[classification][poi_type]
            for poi_data in pois:
                points = poi_data['points']
                for point in points:
                    distance = determineRadiusDistance(lat, lon, point[0], point[1])
                    poi_data['distance'] = distance
                    distances.append(distance)
                    if shortest_distance is None or shortest_distance > distance:
                        shortest_distance = distance
                        shortest_data = poi_data
            if len(distances) > 0:
                shortest_data['average_distance'] = sum(distances) / float(len(distances))
                shortest_data['count'] = len(pois)
            if not shortest_data is None and not shortest_data is None:
                shortest_data['distance'] = shortest_distance
                result[classification][poi_type] = shortest_data
            else:
                result[classification][poi_type] = {}
    return result


# def processPoisDistances(data, lat, lon):
#     result = {}
#     for poi_type in data:
#         shortest_distance = None
#         shortest_data = None
#         distances = []
#         pois = data[poi_type]
#         for poi_data in pois:
#             points = poi_data['points']
#             for point in points:
#                 distance = determineRadiusDistance(lat, lon, point[0], point[1])
#                 distances.append(distance)
#                 if shortest_distance is None or shortest_distance > distance:
#                     shortest_distance = distance
#                     shortest_data = poi_data
#         if len(distances) > 0:
#             shortest_data['average_distance'] = sum(distances) / float(len(distances))
#             shortest_data['count'] = len(pois)
#         if not shortest_data is None and not shortest_data is None:
#             shortest_data['distance'] = shortest_distance
#             result[poi_type] = shortest_data
#         else:
#             result[poi_type] = {}
#     return result
