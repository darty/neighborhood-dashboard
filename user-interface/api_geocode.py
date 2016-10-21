from geopy.geocoders import Nominatim

def reverse_geocode(lat, lon):
    geolocator = Nominatim()
    location = geolocator.reverse("{}, {}".format(lat, lon))
    return location.address