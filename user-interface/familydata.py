import csv

from common import *

# SSO Clean #
def readSSOClean(sso_clean_file):
    sso_data = {}
    family_data_col = 0
    header_index = {}
    printHeadline('Reading SSO Clean information from %s' % (sso_clean_file))
    with open(sso_clean_file, 'r') as csvfile:
        sso_clean_reader = csv.reader(csvfile, delimiter=';')
        header_row = next(sso_clean_reader)
        i = 0
        for col in header_row:
            if col == "familyid":
                family_data_col = i
            else:
                header_index[i] = col
            i += 1
        for row in sso_clean_reader:
            details = {}
            familyid = row[family_data_col]
            try:
                for key, value in header_index.iteritems():
                    details[value] = row[key]
                sso_data[familyid] = details
            except ValueError:
                print 'Not an integer: %s' % (familyid)
    return sso_data

# C-STRENGTH DATA #
def readCstrengths(cstrengthsfile):
    sso_data = {}
    printHeadline('Reading C-Strengths information from %s' % (cstrengthsfile))
    # print 'Reading C-Strengths from:', cstrengthsfile
    with open(cstrengthsfile, 'r') as csvfile:
        cstrengthreader = csv.reader(csvfile, delimiter=';')
        for row in cstrengthreader:
            details = {}
            familyid = row[0]
            try:
                int(familyid)
                details['P12CACORNCategory'] = row[1]
                details['P12HealthACORN07Group'] = row[2]
                details['SSO_PdisorderC'] = row[3]
                details['SSO_PdecayC'] = row[4]
                details['SSO_NightUnsafe'] = row[5]
                details['SSO_NEIGHSAFEr'] = row[6]
                details['SSO_StreetSAFE'] = row[7]
                details['SSO_neighKids'] = row[8]
                details['density'] = row[9]
                details['PerGreen'] = row[10]
                details['numGreen'] = row[11]
                sso_data[familyid] = details
            except ValueError:
                print 'Not an integer %s' % (familyid)
    return sso_data


def readCoordinates(coordinatesfile):
    location_data = {}
    family_data_col = -1
    latitude_col = -1
    longitude_col = -1

    printHeadline('Reading Family coordinate information from %s' % (coordinatesfile))
    with open(coordinatesfile, 'r') as csvfile:
        familyreader = csv.reader(csvfile, delimiter=',')
        header_row = next(familyreader)
        i = 0
        for col in header_row:
            if col == "familyid":
                family_data_col = i
            elif "longitude" in col:
                longitude_col = i
            elif "latitude" in col:
                latitude_col = i
            else:
                print 'WARNING Unknown column', col
            i += 1
        if latitude_col == -1 or longitude_col == -1:
            print "Error determining coordinate columns", latitude_col, longitude_col
        j = 0
        for row in familyreader:
            print row
            id = 0
            if not family_data_col == -1:
                id = row[family_data_col]
            else:
                id = j
                j += 1
            try:
                int(id)
                point = {}
                point["latitude"] = row[latitude_col]
                point["longitude"] = row[longitude_col]
                location_data[id] = point
            except ValueError:
                print 'Not an integer %s' % (id)
    return location_data
