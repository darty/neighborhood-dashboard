from common import *

def writePoint(name, long, lat, f):
    f.write("\t<Placemark>\n")
    f.write("\t\t<name>" + name + "</name>\n")
    f.write("\t\t<Point>\n")
    f.write("\t\t\t<coordinates>" + long + "," + lat + ",0.0 </coordinates>\n")
    f.write("\t\t</Point>\n")
    f.write("\t</Placemark>\n")

def writeRing(name, points, f):
    f.write("\t<Placemark>\n")
    f.write("\t\t<name>" + name + "</name>\n")
    f.write("\t\t<Style>\n")
    f.write("\t\t\t<LineStyle><color>ff0000ff</color><width>2</width></LineStyle>\n")
    f.write("\t\t\t<PolyStyle><fill>0</fill><outline>1</outline></PolyStyle>\n")
    f.write("\t\t</Style>\n")
    f.write("\t\t<Polygon><outerBoundaryIs><LinearRing>\n")
    f.write("\t\t\t<coordinates>\n")
    f.write("\t\t\t")
    for p in points:
        f.write("" + str(p[1]) + "," + str(p[0]) + ",0.0 ")
    f.write("\n")
    f.write("\t\t\t</coordinates>\n")
    f.write("\t\t</LinearRing></outerBoundaryIs></Polygon>\n")
    f.write("\t</Placemark>\n")

def writeFamilyKML(family, location_data, road_data):
    points = road_data['points']

    filepath = os.path.join(KMLFOLDER, family + '_debug.kml')
    f = open(filepath, 'w')
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
    f.write("<Document>\n")
    f.write("\t<name>" + filepath +"</name>\n")
    f.write("\t<Placemark>\n")
    f.write("\t\t<name>Home Location</name>\n")
    f.write("\t\t<Point>\n")
    f.write("\t\t\t<coordinates>" + location_data['longitude'] + "," + location_data['latitude'] + ",0.0 </coordinates>\n")
    f.write("\t\t</Point>\n")
    f.write("\t</Placemark>\n")

    f.write("\t<Placemark>\n")
    f.write("\t\t<name>Road</name>\n")
    f.write("\t\t<Style>\n")
    f.write("\t\t\t<LineStyle><color>ff0000ff</color><width>2</width></LineStyle>\n")
    f.write("\t\t\t<PolyStyle><fill>0</fill><outline>1</outline></PolyStyle>\n")
    f.write("\t\t</Style>\n")

    f.write("\t\t<Polygon><outerBoundaryIs><LinearRing>\n")
    f.write("\t\t\t<coordinates>\n")
    f.write("\t\t\t")
    for p in points:
        f.write("" + str(p[1]) + "," + str(p[0]) + ",0.0 ")
    f.write("\n")
    f.write("\t\t\t</coordinates>\n")
    f.write("\t\t</LinearRing></outerBoundaryIs></Polygon>\n")
    f.write("\t</Placemark>\n")

    f.write("</Document>\n")
    f.write("</kml>\n")
    f.close()

def writeDebugKML(location_data, road_data):
    if not os.path.exists(KMLFOLDER):
        os.makedirs(KMLFOLDER)
    filepath = os.path.join(KMLFOLDER, 'output.kml')
    f = open(filepath, 'w')
    f.write("<?xml version='1.0' encoding='UTF-8'?>\n")
    f.write("<kml xmlns='http://earth.google.com/kml/2.1'>\n")
    f.write("<Document>\n")
    f.write("\t<name>" + filepath +"</name>\n")
    for family in location_data:
        # writeFamilyKML(family, location_data[family], road_data[family])
        writePoint(family + " Home Location", location_data[family]['longitude'], location_data[family]['latitude'], f)
        writeRing(family + "Road", road_data[family]['points'], f)
    f.write("</Document>\n")
    f.write("</kml>\n")
    f.close()