import urllib2
import json
import time

WALKABILITY_BASE_URI = "http://api.walkscore.com/score?format=json"
TRANSIT_BASE_URI = "http://transit.walkscore.com/transit/score/"
LAT_PART = "lat="
LON_PART = "lon="
API_PART = "wsapikey="


def request_walkability(lat, lon, api_key):
    uri = WALKABILITY_BASE_URI
    uri += "&" + LAT_PART + str(lat)
    uri += "&" + LON_PART + str(lon)
    uri += "&" + API_PART + str(api_key)
    print uri

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
            if 'status' in result and result['status'] == 1:
                return result
            if 'status' in result and result['status'] == 2:
                # wait a bit
                print 'Waiting a few seconds for the walkability score'
                time.sleep(5)
                if count > 5:
                    print 'Tried too many times'
                    return None
                count += 1


def request_transit_score(lat, lon, api_key):
    uri = TRANSIT_BASE_URI
    uri += "?" + LAT_PART + str(lat)
    uri += "&" + LON_PART + str(lon)
    uri += "&" + API_PART + str(api_key)
    uri += "&city=chesapeake&state=VA"

    retry = True
    while retry:
        try:
            socket = urllib2.urlopen(uri)
        except urllib2.HTTPError as e:
            print 'The server couldn\'t fulfill the request. Error code: ', e.code
            return None
        except urllib2.URLError as e:
            print 'We failed to reach a server. Reason: ', e.reason
        else:
            reply = socket.read()
            result = json.loads(reply)
            print result
            print result['status']
            if 'status' in result and result['status'] == 1:
                retry = False
                return result
                # else:

if __name__ == "__main__":
    request_walkability(40.176829, -76.817628, "fa7cd0bad457d24e2047b0c756136197")
    #request_transit_score(40.176829, -76.817628, "fa7cd0bad457d24e2047b0c756136197")
    request_transit_score(36.788110, -76.281043, "fa7cd0bad457d24e2047b0c756136197")
    #request_walkability(49.2574503,7.0447988, "fa7cd0bad457d24e2047b0c756136197")