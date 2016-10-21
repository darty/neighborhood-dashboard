from pykml import parser
from lxml import etree
from geopy.distance import vincenty
from common import *
import os

CSV_ROAD_DIFFERENCE_FIELDNAMES = [ 'familyid', 'orig_length', 'nd_length', 'difference' ]

def calculateDistance(p1, p2):
    distance = vincenty(p1, p2).meters
    return distance

def calculateLength(points):
    result = 0
    p1 = points[0]
    for i in range(1, len(points)):
        p2 = points[i]
        result += calculateDistance(p1, p2)
        p1 = p2
    return result

def compareResults(orig_result, nd_result, outputfile):
    orig_keys = set(orig_result.keys())
    nd_keys = set(nd_result.keys())

    not_in_nd = orig_keys - nd_keys # In KML excluding those in the CSV
    not_in_orig = nd_keys - orig_keys # In CSV excluding those in KML

    print "In KML excluding those in the CSV (ND)", len(not_in_nd)
    for key in not_in_nd:
        print key,#, orig_result[key]

    print ''
    print "In CSV excluding those in KML (Orig)", len(not_in_orig)
    for key in not_in_orig:
        print key,#, nd_result[key]

    common_keys = orig_keys & nd_keys

    difference_rows = []

    for k in common_keys:
        orig_length = calculateLength(orig_result[k])
        nd_length = calculateLength(nd_result[k])
        # print k, orig_length, nd_length
        diff = {
            'familyid': k,
            'orig_length': orig_length,
            'nd_length': nd_length,
            'difference': orig_length - nd_length
        }
        difference_rows.append(diff)

    initCSV(outputfile, CSV_ROAD_DIFFERENCE_FIELDNAMES)
    appendCSV(difference_rows, outputfile, CSV_ROAD_DIFFERENCE_FIELDNAMES)


def readNdFolder(foldername):
    if not os.path.exists(foldername):
        return {}
    onlyfiles = [f for f in os.listdir(foldername) if os.path.isfile(os.path.join(foldername, f))]
    result = {}
    for f in onlyfiles:
        [name, ext] = str(f).split(".")
        fullpath = os.path.join(foldername, f)
        with open(fullpath) as kmlfile:
            kmldoc = parser.parse(kmlfile)
            root = kmldoc.getroot()
            coords = []
            for x in root.Document.Placemark:
                [lat, lon, h] = str(x.Point.coordinates).rstrip().lstrip().split(",")
                coords.append([float(lat), float(lon)])
            if int(name) in result.keys():
                print "Error: key in ND already exists!", name, result[int(name)], coords
            result[int(name)] = coords
    return result


def readOrigFolder(foldername):
    if not os.path.exists(foldername):
        return {}
    onlyfiles = [f for f in os.listdir(foldername) if os.path.isfile(os.path.join(foldername, f))]
    result = {}
    for f in onlyfiles:
        fullpath = os.path.join(foldername, f)
        with open(fullpath) as kmlfile:
            kmldoc = parser.parse(kmlfile)
            root = kmldoc.getroot()
            for x in root.Document.Folder.Placemark:
                # print etree.tostring(x, pretty_print=True)
                coords = [y for y in str(x.LineString.coordinates).rstrip().lstrip().split(" ")]
                coords_filtered = []
                for y in coords:
                    lat, lon, h = y.split(",")
                    coords_filtered.append([float(lat), float(lon)])
                    #if "Path" in str(x.name) or "Line" in x.name or "," in str(x.name) or "." in str(x.name):
                     #   print x.name
                try:
                    name = str(x.name).replace("Path", "").replace("Line", "").replace(",", "").replace(".", "").rstrip().lstrip()
                    #if int(name) in result.keys():
                    #    print "Error: key in orig already exists!", name, result[int(name)], coords
                    result[int(name)] = coords_filtered
                except:
                    print "##################", fullpath, x.name
    return result


if __name__ == "__main__":
    basefolder = 'road_analysis'
    origfolder = 'orig'
    ndfolder = 'nd_phase4'
    outputfile = 'results_phase4.csv'
    orig_result = readOrigFolder(os.path.join(basefolder, origfolder))
    nd_result = readNdFolder(os.path.join(basefolder, ndfolder))
    compareResults(orig_result, nd_result, os.path.join(basefolder, outputfile))
