import json
import time

from common import *

WALKABILITY_BASE_URI = "http://api.walkscore.com/score?format=json"
TRANSIT_BASE_URI = "http://transit.walkscore.com/transit/score/"
LAT_PART = "lat="
LON_PART = "lon="
API_PART = "wsapikey="
CITY_PART = "city="
STATE_PART = "state="

def perform_request(uri, wait_for_status=False):
    count = 0
    retry = True
    while retry:
        try:
            uri2 = uri + "&" + 'date=' + str(int(time.time()))
            socket = urllib2.urlopen(uri2)
        except urllib2.HTTPError as e:
            print 'The server couldn\'t fulfill the request. Error code: ', e.code
            return None
        except urllib2.URLError as e:
            print 'We failed to reach a server. Reason: ', e.reason
            return None
        else:
            reply = socket.read()
            result = json.loads(reply)
            print result
            if not wait_for_status or ('status' in result and result['status'] == 1):
                return result
            if 'status' in result and result['status'] == 2:
                # wait a bit
                print 'Waiting a few seconds for the result'
                time.sleep(5)
                if count > 5:
                    print 'Tried too many times'
                    return None
                count += 1


def request_walkability(lat, lon, api_key):
    uri = WALKABILITY_BASE_URI
    uri += "&" + LAT_PART + str(lat)
    uri += "&" + LON_PART + str(lon)
    uri += "&" + API_PART + str(api_key)
    #print uri
    return perform_request(uri, True)

def request_transit_score(lat, lon, revgeo, api_key):
    country = revgeo['address']['country_code']
    if not 'us' in country:
        return None
    city = revgeo['address']['city']
    state = revgeo['address']['state_district']
    uri = TRANSIT_BASE_URI
    uri += "?" + LAT_PART + str(lat)
    uri += "&" + LON_PART + str(lon)
    uri += "&" + API_PART + str(api_key)
    uri += "&" + CITY_PART + str(city)
    uri += "&" + STATE_PART + str(state)
    #print uri
    return perform_request(uri)

def writeWalkabilityHeadersToCsv(csvfolder, filename):
    if not os.path.exists(csvfolder):
        os.makedirs(csvfolder)
    initCSV(os.path.join(csvfolder, filename), CSV_WALKABILITY_FIELDNAMES)


def writeWalkabilityDictionaryToCsv(data, csvfolder, filename):
    if not os.path.exists(csvfolder):
        os.makedirs(csvfolder)
    # new_data = {}
    # for key in CSV_WALKABILITY_FIELDNAMES:
    #     if key in data:
    #         new_data[key] = data[key]
    #     else:
    #         new_data[key] = ''
    appendCSV(data, os.path.join(csvfolder, filename), CSV_WALKABILITY_FIELDNAMES)


if __name__ == "__main__":
    print 'Not like this'

