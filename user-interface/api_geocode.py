from geopy.geocoders import Nominatim

def reverse_geocode(lat, lon):
    geolocator = Nominatim()
    location = geolocator.reverse("{}, {}".format(lat, lon))
    return location


if __name__ == "__main__":
    result = reverse_geocode('51.55447', '0.8025423')
    print result.raw['address']['country_code']