#!/usr/bin/python
# __author__ = 'ddegraen'
import sys
import getopt
import json
import datetime

from distutils.dir_util import copy_tree

from common import *
import familydata
import policedata
import osmroad
import streetsign_detection
import urbanicitydata

location_data = {}
sso_data = {}
police_data = {}
road_data = {}
category_data = {}
urbanicity_data = {}


def printUsage():
    print '###########################################################################################################'
    print os.path.dirname(os.path.realpath('__file__')), '-l <coordinatesfile> -s <sso_clean_file> -o <outputfolder> -y <year> -k -n'
    print '###########################################################################################################'
    print 'Arguments:'
    print '-h: Show this help'
    print '-l <filename>: Name of the coordinates file. Has to be a csv file with cols [familyid, latitude, longitude]'
    print '-s <filename>: Name of the SSO file. Has to be a csv file with variable cols (required col is familyid)'
    print '-o <folder>: Output folder where to put the results. Preferably html/data'
    print '-y <year>: Year to request the crimedata.'
    print '-k: Create the KML files containing the locations and headings per family.'
    print '-n: Do not perform any fake requests.'
    print '###########################################################################################################'
    print 'Example for trunked dataset:'
    # print os.path.basename(__file__), '-l A12-XY-trunked.csv -s SSOclean-trunked.csv -o html/data -y 2012 -k -n'
    print os.path.dirname(os.path.realpath('__file__')), '-l A12-XY-trunked.csv -s SSOclean-trunked.csv -o html/data -y 2012 -k -n'
    print 'Example for complete dataset:'
    # print os.path.basename(__file__), '-l A12-XY.csv -s SSOclean.csv -o html/data -y 2012 -k -n'
    print os.path.dirname(os.path.realpath('__file__')), '-l A12-XY.csv -s SSOclean.csv -o html/data -y 2012 -k -n'
    print '###########################################################################################################'


def writeObject(varname, data, folder, filename, callback=''):
    if not os.path.exists(folder):
        os.makedirs(folder)
    outputfile = os.path.join(folder, filename)
    with open(outputfile, 'w') as output:
        output.write('var ' + varname + ' = ')
        output.write(json.dumps(data))
        output.write(';\n')
        if callback != '':
            output.write(callback)
            output.write('(' + varname + ');\n')


# WRITE OUTPUT #
def writeOutput(outputfolder):
    if location_data:
        writeObject('LOCATION_DATA', location_data, outputfolder, 'location-data.js')
    if sso_data:
        ssofolder = os.path.join(outputfolder, SSO_PATH)
        writeObject('SSO_DATA', sso_data, ssofolder, 'sso-data.js')
    if police_data:
        policefolder = os.path.join(outputfolder, POLICE_PATH)
        for family in police_data:
            family_data = police_data[family]
            writeObject('POLICE_DATA', family_data, policefolder, 'police-data-' + family + '.js', 'loadCrimesCallback')
    if road_data:
        roadfolder = os.path.join(outputfolder, ROAD_PATH)
        for family in road_data:
            family_data = road_data[family]
            writeObject('ROAD_DATA', family_data, roadfolder, 'road-data-' + family + '.js', 'loadRoadCallback')
    if category_data:
        policefolder = os.path.join(outputfolder, POLICE_PATH)
        writeObject('CATEGORY_DATA', category_data, policefolder, 'category-data.js')


def writeCommonFiles(location_data, sso_data, category_data, outputfolder):
    if location_data:
        writeObject('LOCATION_DATA', location_data, outputfolder, 'location-data.js')
    if sso_data:
        ssofolder = os.path.join(outputfolder, SSO_PATH)
        writeObject('SSO_DATA', sso_data, ssofolder, 'sso-data.js')
    if category_data:
        policefolder = os.path.join(outputfolder, POLICE_PATH)
        writeObject('CATEGORY_DATA', category_data, policefolder, 'category-data.js')


def writeFamilyData(family, lat, lon, police_data, road_data, detection_data, outputfolder):
    if police_data:
        policefolder = os.path.join(outputfolder, POLICE_PATH)
        writeObject('POLICE_DATA', police_data, policefolder, 'police-data-' + str(family) + '.js', 'loadCrimesCallback')
    if road_data:
        roadfolder = os.path.join(outputfolder, ROAD_PATH)
        writeObject('ROAD_DATA', road_data, roadfolder, 'road-data-' + str(family) + '.js', 'loadRoadCallback')
    if detection_data:
        detectionfolder = os.path.join(outputfolder, DETECTION_PATH)
        writeObject('DETECTION_DATA', detection_data, detectionfolder, 'detection-data-' + str(family) + '.js', 'loadDetectionCallback')


def runPreprocessing(coordinatesfile, ssocleanfile, urbanicityfile, outputfolder, year, fake_requests, no_detection, road_points):
    global location_data
    global sso_data
    global police_data
    global road_data
    global category_data
    global urbanicity_data
    printHeadline('Preprocessing year %s files: %s %s to output %s' % (year, coordinatesfile, ssocleanfile, outputfolder))

    process_urbanicity = False
    if not urbanicityfile is None:
        process_urbanicity = True

    # Copy base files
    fromDirectory = HTML_SOURCE_FOLDER
    toDirectory = outputfolder
    copy_tree(fromDirectory, toDirectory)

    # Folder Determinations
    data_output_folder = os.path.join(outputfolder, DATA_FOLDER)
    streetview_output_folder = os.path.join(outputfolder, STREETVIEW_IMAGES_FOLDER)
    osm_output_folder = os.path.join(outputfolder, OSMDATAFOLDER)
    kml_output_folder = os.path.join(outputfolder, KMLFOLDER)
    kml_road_output_folder = os.path.join(outputfolder, KMLROADFOLDER)
    csvfolder = os.path.join(outputfolder, CSV_PATH)

    location_data = familydata.readCoordinates(coordinatesfile)
    if not ssocleanfile is None:
        sso_data = familydata.readSSOClean(ssocleanfile)
    if not year is None:
        category_data = policedata.requestCrimeCategories(year)
    writeCommonFiles(location_data, sso_data, category_data, data_output_folder)

    if process_urbanicity:
        urbanicity_data = urbanicitydata.readUrbanicity(urbanicityfile)

    police_data = {}
    road_data = {}
    detection_data = {}

    policedata.writePoliceHeadersToCsv(csvfolder, 'police_crime_data.csv', 'police_stop_and_search_data.csv')
    osmroad.writeClosestPoiHeadersToCsv(csvfolder, 'closest_poi_data.csv')
    if process_urbanicity:
        urbanicity_fieldnames = urbanicitydata.writeUrbanicityHeadersToCsv(csvfolder, 'urbanicity_data.csv')

    counter = 0
    for family in location_data:
        counter += 1
        printHeadline('%s Processing family %s %s/%s' % (datetime.datetime.now(), family, counter, len(location_data)))
        if not 'latitude' in location_data[family] or not 'longitude' in location_data[family] or not location_data[family]['latitude'] or not location_data[family]['longitude']:
            print 'Family %s does not have a location' % (family)
            continue
        try:
            lat = float(location_data[family]['latitude'])
            lon = float(location_data[family]['longitude'])
        except:
            print 'Could not convert coordinates to float for family %s' % (family)
            continue
        fake_count = 0
        if fake_requests:
            fake_count = FAKE_REQUESTS_COUNT # * len(location_data)
        random_locations = getRandomLocations(lat, lon, fake_count)

        road_data = osmroad.retrieveFamilyRoads(family, lat, lon, list(random_locations), osm_output_folder)
        osmroad.writeClosestPoiToCsv(family, lat, lon, road_data['closest_pois'], csvfolder, 'closest_poi_data.csv')
        if process_urbanicity:
            data = {}
            if family in urbanicity_data:
                data = urbanicity_data[family]
            urbanicitydata.writeUrbanicityRowToCsv(family, data, road_data['closest_pois'], csvfolder, 'urbanicity_data.csv', urbanicity_fieldnames)

        policefolder = os.path.join(data_output_folder, POLICE_PATH)
        policefile = os.path.join(policefolder, 'police-data-' + str(family) + '.js')

        if os.path.isfile(policefile):
            print 'Skipping police data for %s' % family
        else:
            police_data = policedata.requestFamilyPoliceData(family, lat, lon, year, list(random_locations), road_data['roads']['points'])
            flat_police_crime_data = policedata.flattenPoliceDictionaryCrimes(family, police_data)
            flat_police_stop_and_search_data = policedata.flattenPoliceDictionaryStopAndSearches(family, police_data)
            policedata.writePoliceDictionaryToCsv(flat_police_crime_data, flat_police_stop_and_search_data, csvfolder, 'police_crime_data.csv', 'police_stop_and_search_data.csv')

        roadfolder = os.path.join(data_output_folder, ROAD_PATH)
        roadfile = os.path.join(roadfolder, 'road-data-' + str(family) + '.js')

        if os.path.isfile(roadfile) and streetsign_detection.checkDetectionDone(family, streetview_output_folder):
            print 'Skipping road data for %s' % family
        else:
            family_point_data = osmroad.determineRoadPoints(family, road_data)
            detection_data = None
            if not no_detection:
                detection_data = streetsign_detection.determineStreetSigns(family, family_point_data, streetview_output_folder)
            if road_points:
                osmroad.writeFamilyKmlPoints(family, family_point_data, kml_output_folder)
                osmroad.writeRoadKmlPoints(family, road_data, kml_road_output_folder)
        writeFamilyData(family, lat, lon, police_data, road_data, detection_data, data_output_folder)


if __name__ == "__main__":
    coordinatesfile = ''
    ssocleanfile = None
    urbanicityfile = None
    outputfolder = ''
    road_points = False
    fake_requests = True
    no_detection = False
    year = YEAR
    try:
        opts, args = getopt.getopt(sys.argv[1:],"hl:o:y:s:u:knd",["lfile=","ofile=","year=","sfile=","ufile"])
        for opt, arg in opts:
            if opt == '-h':
                printUsage()
                sys.exit(0)
            elif opt == '-k':
                road_points = True
            elif opt == '-n':
                fake_requests = False
            elif opt == '-d':
                no_detection = True
            elif opt in ("-l", "--lfile"):
                coordinatesfile = arg
            elif opt in ("-o", "--ofile"):
                outputfolder = arg
            elif opt in ("-y", "--year"):
                year = arg
            elif opt in ("-s", "--sfile"):
                ssocleanfile = arg
            elif opt in ("-u", "--ufile"):
                urbanicityfile = arg
    except getopt.GetoptError:
        print 'Error: '
        printUsage()
        sys.exit(2)
    runPreprocessing(coordinatesfile, ssocleanfile, urbanicityfile, outputfolder, year, fake_requests, no_detection, road_points)
