import json
import ssl
#import csv
#import urllib2
#import math
#import random

from common import *

# POLICE DATA URI #
def requestPoliceURI(baseuri, lat, lon, year, month):
    uri = baseuri + 'lat=' + str(lat) + '&lng=' + str(lon)
    uri += '&date=' + str(year) + '-'
    if month < 10:
        uri += '0'
    uri += str(month)
    context = ssl._create_unverified_context()
    r = urllib2.urlopen(uri, context=context)
    if r is None:
        print 'No results for uri %s' % (uri)
        return {}
    return json.load(r)


def requestFilteredData(base_uri, lat, lon, year, polygon, family_road_points):
    result = {}
    for i in range(0, 12):
        crimes = requestPoliceURI(base_uri, lat, lon, year, i+1)
        filtered_crimes = []
        if polygon is None:
            filtered_crimes = crimes
        else:
            for crime in crimes:
                try:
                    if 'location' in crime and 'latitude' in crime['location'] and 'longitude' in crime['location']:
                        crimeLocation = crime['location']
                        crimeLat = float(crimeLocation['latitude'])
                        crimeLon = float(crimeLocation['longitude'])
                        if point_inside_polygon(crimeLat, crimeLon, polygon):
                            crime['on_family_road'] = point_on_segments(crimeLat, crimeLon, family_road_points)
                            filtered_crimes.append(crime)
                except ValueError:
                    continue
        print '(%s:%i/%i);' % (MONTHS[i], len(filtered_crimes), len(crimes)),
        result[i] = filtered_crimes
    return result


def requestData(lat, lon, year, polygon, family_road_points):
    result = {}
    print '# Crimes',
    result['crimes'] = requestFilteredData(CRIME_URI, lat, lon, year, polygon, family_road_points)
    print ''
    print '# Stop And Searches',
    result['stop_and_search'] = requestFilteredData(STOP_AND_SEARCH_URI, lat, lon, year, polygon, family_road_points)
    print ''
    return result


# Individual Police Data
def requestFamilyPoliceData(family, lat, lon, year, random_locations, family_road_points):
    # printHeadline('Processing Police Data for (%s,%s)' %(lat,lon))
    random.seed()
    family_done = False
    police_data = {}
    active = True
    while active:
        rnd = random.randint(0, FAKE_REQUESTS_COUNT)
        if rnd > 0 and len(random_locations) > 0:
            # rnd location
            fake_location = random_locations.pop(random.randint(0, len(random_locations) - 1))
            print 'Fake police request %s' % (fake_location)
            requestData(fake_location[0], fake_location[1], year, None, family_road_points)
        elif not family_done:
            # actual location
            polygon = determinePolygon(lat, lon)
            print 'Processing police data for family %s at (%s,%s)' % (family, lat, lon)
            police_data = requestData(lat, lon, year, polygon, family_road_points)
            family_done = True
        if family_done and len(random_locations) == 0:
            active = False
    return police_data

# def requestPoliceDataAll(location_data, year, random_locations):
#     printHeadline('Processing Police Data')
#     random.seed()
#     actual_locations = list(location_data.keys())
#     police_data = {}
#     active = True
#     while active:
#         rnd = random.randint(0, FAKE_REQUESTS_COUNT)
#         if rnd > 0 and len(random_locations) > 0:
#             # rnd location
#             fake_location = random_locations.pop(random.randint(0, len(random_locations) - 1))
#             print 'Processing fake location %s' % (fake_location)
#             requestData(fake_location[0], fake_location[1], year, None, family_road_points)
#         else:
#             # actual location
#             family = actual_locations.pop(random.randint(0, len(actual_locations) - 1))
#             if not 'latitude' in location_data[family] or not 'longitude' in location_data[family]:
#                 print 'Family %s does not have a location:' % (family), 'Removing %d fake locations.' % (FAKE_REQUESTS_COUNT)
#                 for i in range(FAKE_REQUESTS_COUNT):
#                     random_locations.pop(random.randint(0, len(random_locations) - 1))
#                 continue
#             lat = location_data[family]['latitude']
#             lon = location_data[family]['longitude']
#             polygon = determinePolygon(float(lat), float(lon))
#             print 'Processing family %s at (%s,%s)' % (family, lat, lon)
#             police_data[family] = requestData(lat, lon, year, polygon, family_road_points)
#         if len(actual_locations) == 0 and len(random_locations) == 0:
#             active = False
#     return police_data

def requestCrimeCategories(year):
    result = {}
    for i in range(0, 12):
        uri = CATEGORY_URI + str(year) + '-'
        if i+1 < 10:
            uri += '0'
        uri += str(i+1)
        context = ssl._create_unverified_context()
        r = urllib2.urlopen(uri, context=context)
        if r is None:
            print 'No results for uri %s' % (uri)
            continue
        categories = json.load(r)
        for category in categories:
            curl = category['url']
            if not curl in result:
                result[curl] = category['name']
    return result

def flattenPoliceDictionaryStopAndSearches(family, police_data):
    result = []
    stop_and_searches = police_data['stop_and_search']
    for key in stop_and_searches:
        for stop_and_search in stop_and_searches[key]:
            latitude = None
            longitude = None
            street_id = None
            street_name = None
            if 'location' in stop_and_search and not stop_and_search['location'] is None:
                latitude = stop_and_search['location']['latitude']
                longitude = stop_and_search['location']['longitude']
                if 'street' in stop_and_search['location']:
                    street_id = stop_and_search['location']['street']['id']
                    street_name = stop_and_search['location']['street']['name']
            row = {
                'family_id': family,
                'data_type': 'stop_and_search',
                'type': stop_and_search['type'],
                'involved_person': stop_and_search['involved_person'],
                'datetime': stop_and_search['datetime'],
                'operation': stop_and_search['operation'],
                'operation_name': stop_and_search['operation_name'],
                'location_latitude': latitude,
                'location_longitude': longitude,
                'location_street_id': street_id,
                'location_street_name': street_name,
                'gender': stop_and_search['gender'],
                'age_range': stop_and_search['age_range'],
                'self_defined_ethnicity': stop_and_search['self_defined_ethnicity'],
                'officer_defined_ethnicity': stop_and_search['officer_defined_ethnicity'],
                'legislation': stop_and_search['legislation'],
                'object_of_search': stop_and_search['object_of_search'],
                'outcome': stop_and_search['outcome'],
                'outcome_linked_to_object_of_search': stop_and_search['outcome_linked_to_object_of_search'],
                'removal_of_more_than_outer_clothing': stop_and_search['removal_of_more_than_outer_clothing'],
                'on_family_road': stop_and_search['on_family_road']
            }
            result.append(row)
    return result

def flattenPoliceDictionaryCrimes(family, police_data):
    result = []
    crimes = police_data['crimes']
    for key in crimes:
        for crime in crimes[key]:
            latitude = None
            longitude = None
            street_id = None
            street_name = None
            if 'location' in crime and not crime['location'] is None:
                latitude = crime['location']['latitude']
                longitude = crime['location']['longitude']
                if 'street' in crime['location']:
                    street_id = crime['location']['street']['id']
                    street_name = crime['location']['street']['name']
            outcome_status_category = None
            outcome_status_date = None
            if 'outcome_status' in crime and not crime['outcome_status'] is None:
                outcome_status_category = crime['outcome_status']['category']
                outcome_status_date = crime['outcome_status']['date']
            row = {
                'family_id': family,
                'data_type': 'crime',
                'category': crime['category'],
                'persistent_id': crime['persistent_id'],
                'month': crime['month'],
                'location_latitude': latitude,
                'location_longitude': longitude,
                'location_street_id': street_id,
                'location_street_name': street_name,
                'context': crime['category'],
                'id': crime['id'],
                'location_type': crime['location_type'],
                'location_subtype': crime['location_subtype'],
                'outcome_status_category': outcome_status_category,
                'outcome_status_date': outcome_status_date,
                'on_family_road': crime['on_family_road']
                  }
            result.append(row)
    return result

def writePoliceHeadersToCsv(csvfolder, crimefilename, stopandsearchfilename):
    if not os.path.exists(csvfolder):
        os.makedirs(csvfolder)
    initCSV(os.path.join(csvfolder, crimefilename), CSV_CRIME_FIELDNAMES)
    initCSV(os.path.join(csvfolder, stopandsearchfilename), CSV_STOPANDSEARCH_FIELDNAMES)

def writePoliceDictionaryToCsv(crime_data, stopandsearch_data, csvfolder, crimefilename, stopandsearchfilename):
    if not os.path.exists(csvfolder):
        os.makedirs(csvfolder)
    appendCSV(crime_data, os.path.join(csvfolder, crimefilename), CSV_CRIME_FIELDNAMES)
    appendCSV(stopandsearch_data, os.path.join(csvfolder, stopandsearchfilename), CSV_STOPANDSEARCH_FIELDNAMES)