from common import *

def readUrbanicity(urbanicityfile):
    urbanicity_data = {}
    family_data_col = 0
    header_index = {}
    printHeadline('Reading Urbanicity information from %s' % (urbanicityfile))
    with open(urbanicityfile, 'r') as csvfile:
        urbanicity_reader = csv.reader(csvfile, delimiter=';')
        header_row = next(urbanicity_reader)
        i = 0
        for col in header_row:
            if col == "familyid":
                family_data_col = i
            else:
                header_index[i] = col
            i += 1
        for row in urbanicity_reader:
            details = {}
            familyid = row[family_data_col]
            try:
                for key, value in header_index.iteritems():
                    details[value] = row[key]
                urbanicity_data[familyid] = details
            except ValueError:
                print 'Not an integer: %s' % (familyid)
    return urbanicity_data


def writeUrbanicityHeadersToCsv(csvfolder, filename):
    if not os.path.exists(csvfolder):
        os.makedirs(csvfolder)
    fieldnames = CSV_URBANICITY_POI_FIELDNAMES
    for key in CSV_URBANICITY_VARIABLES:
        fieldnames.append('count_' + key)
        fieldnames.append('avg_' + key)
        fieldnames.append('closest_' + key)
    initCSV(os.path.join(csvfolder, filename), fieldnames)
    return fieldnames


def writeUrbanicityRowToCsv(family, urbanicity_data, closest_pois, csvfolder, filename, fieldnames):
    if not os.path.exists(csvfolder):
        os.makedirs(csvfolder)
    csv_data = urbanicity_data.copy()
    csv_data['familyid'] = family
    for classification in closest_pois:
        for key in CSV_URBANICITY_VARIABLES:
            if key in closest_pois[classification]:
                poi_data = closest_pois[classification][key]
                csv_data['count_'+key] = poi_data['count']
                csv_data['closest_'+key] = poi_data['distance']
                csv_data['avg_'+key] = poi_data['average_distance']
    appendCSV(csv_data, os.path.join(csvfolder, filename), fieldnames)