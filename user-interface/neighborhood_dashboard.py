import os
import json
import ConfigParser
import datetime

from distutils.dir_util import copy_tree

from common import *

import familydata
import policedata
import osmroad
# Py2Exe disable
#'''''
import streetsign_detection
#'''''
# Py2Exe disable end
import urbanicitydata

import api_geocode
import api_walkability


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


def writeCommonFiles(location_data, sso_data, category_data, outputfolder):
    if location_data:
        writeObject('LOCATION_DATA', location_data, outputfolder, 'location-data.js')
    if sso_data:
        ssofolder = os.path.join(outputfolder, SSO_PATH)
        writeObject('SSO_DATA', sso_data, ssofolder, 'sso-data.js')
    if category_data:
        policefolder = os.path.join(outputfolder, POLICE_PATH)
        writeObject('CATEGORY_DATA', category_data, policefolder, 'category-data.js')


def writeGenericFile(generic_data, outputfolder):
    if generic_data:
        writeObject('GENERIC_DATA', generic_data, outputfolder, 'generic-data.js')


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


class NeighborhoodDashboard:

    def __init__(self, config_file):
        printHeadline('Loading config %s' % (config_file))
        # Load configuration
        self.config = ConfigParser.RawConfigParser(allow_no_value=True)
        self.config.read(config_file)

        self.walkability_key = self.get_secure_config('api-keys', 'walkability', None)
        self.perform_walkability = self.walkability_key is not None and not (self.walkability_key == 'None')

        self.generic_data = {}
        self.location_data = {}
        self.sso_data = {}
        self.category_data = {}
        self.urbanicity_data = {}

    def get_secure_config(self, section, option, default):
        if not self.config.has_option(section, option):
            return default
        return self.config.get(section, option)

    def create_directories(self):
        # Prepare input and output folders
        from_directory = HTML_SOURCE_FOLDER
        self.output_directory = self.get_secure_config('settings', 'output-directory', DEFAULT_OUTPUT_FOLDER)
        copy_tree(from_directory, self.output_directory)

        # Folder Determinations
        self.data_output_folder = os.path.join(self.output_directory, DATA_FOLDER)
        self.streetview_output_folder = os.path.join(self.output_directory, STREETVIEW_IMAGES_FOLDER)
        self.osm_output_folder = os.path.join(self.output_directory, OSMDATAFOLDER)
        self.kml_output_folder = os.path.join(self.output_directory, KMLFOLDER)
        self.kml_road_output_folder = os.path.join(self.output_directory, KMLROADFOLDER)
        self.csvfolder = os.path.join(self.output_directory, CSV_PATH)

    def load_input_files(self):
        # Location file loading
        if not self.config.has_option('files', 'location'):
            raise Exception('Location file not configured. Check your config file!')
        location_file = self.config.get('files', 'location')
        if not os.path.isfile(location_file):
            raise Exception('Location file not found. Check if the file exists and check your config file!')
        self.location_data = familydata.readCoordinates(location_file)

        # SSO File loading
        if not self.config.has_option('files', 'sso'):
            print 'SSO file not configured. Continuing without SSO data.'
        sso_file = self.config.get('files', 'sso')
        if not os.path.isfile(sso_file):
            print 'SSO file not found. Check if the file exists and check your config file! Continuing without SSO data.'
        self.sso_data = familydata.readSSOClean(sso_file)

        # Crime data
        if not self.config.has_option('settings', 'year'):
            print 'Year not configured. Continuing without crime data.'
        self.year_setting = self.config.getint('settings', 'year')
        self.category_data = policedata.requestCrimeCategories(self.year_setting)


    def process_generic_data(self, family, lat, lon):
        print "Processing generic data for %s" % family
        data = {}
        data['family_id'] = family
        data['latitude'] = lat
        data['longitude'] = lon
        revgeo = api_geocode.reverse_geocode(lat, lon)
        data['address'] = revgeo.address
        if self.perform_walkability:
            walkability_score = api_walkability.request_walkability(lat, lon, self.walkability_key)
            if not walkability_score is None:
                data['ws_walkscore'] = walkability_score['walkscore']
                data['ws_description'] = walkability_score['description']
                data['ws_link'] = walkability_score['ws_link']
            transit_score = api_walkability.request_transit_score(lat, lon, revgeo.raw, self.walkability_key)
            if not transit_score is None:
                data['ts_transitscore'] = walkability_score['transit_score']
                data['ts_description'] = walkability_score['description']
                data['ts_summary'] = walkability_score['summary']
                data['ts_link'] = walkability_score['ws_link']
        return data

    def run_preprocessing(self):
        printHeadline('Preprocessing ...')

        self.create_directories()
        self.load_input_files()

        writeCommonFiles(self.location_data, self.sso_data, self.category_data, self.data_output_folder)

        # Urbanicity data
        process_urbanicity = self.config.has_option('files', 'urbanicity') and os.path.isfile(self.config.get('files', 'urbanicity'))

        if process_urbanicity:
            self.urbanicity_data = urbanicitydata.readUrbanicity(self.config.get('files', 'urbanicity'))

        policedata.writePoliceHeadersToCsv(self.csvfolder, 'police_crime_data.csv', 'police_stop_and_search_data.csv')
        osmroad.writeClosestPoiHeadersToCsv(self.csvfolder, 'closest_poi_data.csv')
        api_walkability.writeWalkabilityHeadersToCsv(self.csvfolder, 'walkability_data.csv')

        urbanicity_fieldnames = []
        if process_urbanicity:
            urbanicity_fieldnames = urbanicitydata.writeUrbanicityHeadersToCsv(self.csvfolder, 'urbanicity_data.csv')

        fake_count = 0
        if self.get_secure_config('settings', 'fake-requests', DEFAULT_FAKE_REQUESTS) == '1':
            fake_count = int(self.get_secure_config('settings', 'fake-requests-count', DEFAULT_FAKE_REQUESTS_COUNT))

        streetview_detection = self.get_secure_config('settings', 'streetview-detection', DEFAULT_STREETVIEW_DETECTION)
        road_points = self.get_secure_config('debug', 'generate-kml', DEFAULT_ROAD_POINTS)

        gsv_api_key = self.get_secure_config('api-keys', 'gsv', DEFAULT_GSV_KEY)
        if gsv_api_key is None:
            streetview_detection = 0

        counter = 0
        for family in self.location_data:
            counter += 1
            printHeadline(
                '%s Processing family %s %s/%s' % (datetime.datetime.now(), family, counter, len(self.location_data)))
            if not 'latitude' in self.location_data[family] or not 'longitude' in self.location_data[family] or not \
                    self.location_data[family]['latitude'] or not self.location_data[family]['longitude']:
                print 'Family %s does not have a location' % (family)
                continue
            try:
                lat = float(self.location_data[family]['latitude'])
                lon = float(self.location_data[family]['longitude'])
            except:
                print 'Could not convert coordinates to float for family %s' % (family)
                continue
            random_locations = getRandomLocations(lat, lon, fake_count)

            road_data = osmroad.retrieveFamilyRoads(family, lat, lon, list(random_locations), self.osm_output_folder)
            osmroad.writeClosestPoiToCsv(family, lat, lon, road_data['closest_pois'], self.csvfolder,
                                         'closest_poi_data.csv')
            if process_urbanicity:
                family_urbanicity_data = {}
                if family in self.urbanicity_data:
                    family_urbanicity_data = self.urbanicity_data[family]
                urbanicitydata.writeUrbanicityRowToCsv(family, family_urbanicity_data, road_data['closest_pois'],
                                                       self.csvfolder, 'urbanicity_data.csv', urbanicity_fieldnames)

            policefolder = os.path.join(self.data_output_folder, POLICE_PATH)
            policefile = os.path.join(policefolder, 'police-data-' + str(family) + '.js')

            police_data = {}
            if os.path.isfile(policefile):
                print 'Skipping police data for %s' % family
            else:
                police_data = policedata.requestFamilyPoliceData(family, lat, lon, self.year_setting,
                                                                 list(random_locations), road_data['roads']['points'])
                flat_police_crime_data = policedata.flattenPoliceDictionaryCrimes(family, police_data)
                flat_police_stop_and_search_data = policedata.flattenPoliceDictionaryStopAndSearches(family,
                                                                                                     police_data)
                policedata.writePoliceDictionaryToCsv(flat_police_crime_data, flat_police_stop_and_search_data,
                                                      self.csvfolder, 'police_crime_data.csv',
                                                      'police_stop_and_search_data.csv')

            roadfolder = os.path.join(self.data_output_folder, ROAD_PATH)
            roadfile = os.path.join(roadfolder, 'road-data-' + str(family) + '.js')

            detection_data = None

            detection_done = True
            # Py2Exe disable
            # ''''
            detection_done = streetsign_detection.checkDetectionDone(family, self.streetview_output_folder)
            # '''''
            # Py2Exe disable end
            if os.path.isfile(roadfile) and detection_done:
                    print 'Skipping road data for %s' % family
            else:
                family_point_data = osmroad.determineRoadPoints(family, road_data)

                # Py2Exe disable
                #''''
                if streetview_detection == '1':
                    detection_data = streetsign_detection.determineStreetSigns(family, family_point_data,
                                                                                    self.streetview_output_folder, gsv_api_key)
                #'''''
                # Py2Exe disable end

                if road_points == 1:
                    osmroad.writeFamilyKmlPoints(family, family_point_data, self.kml_output_folder)
                    osmroad.writeRoadKmlPoints(family, road_data, self.kml_road_output_folder)
            writeFamilyData(family, lat, lon, police_data, road_data, detection_data, self.data_output_folder)

            self.generic_data[family] = self.process_generic_data(family, lat, lon)
            api_walkability.writeWalkabilityDictionaryToCsv(self.generic_data[family], self.csvfolder, 'walkability_data.csv')

        print self.generic_data
        writeGenericFile(self.generic_data, self.data_output_folder)
