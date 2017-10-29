# script to find peak(s) within range of an origin
# prints sorted list of peaks with known name and elevation
# modify as desired

__author__ = "Moritz Kampelmuehler"

import overpy
import os.path
import dill as pickle
from geopy.geocoders import Nominatim
from geopy.distance import vincenty as distance
import pprint

# specify a radius and address here
radius = 50 * 1e3 # radius to search in in meters
address = "Hauptplatz 1 Graz"

geolocator = Nominatim()
location = geolocator.geocode(address,  addressdetails=True)

filename = "response_{}_{}.pkl".format(address,int(radius/1e3))
if not os.path.isfile(filename):
    api = overpy.Overpass()
    response = api.query("""
        node[natural=peak](around:{}, {}, {});
        out;
        """.format(radius, location.raw['lat'], location.raw['lon']))

    with open(filename, 'wb') as f:
        pickle.dump(response, f)
else:
    with open(filename, 'rb') as f:
        response = pickle.load(f)

peak_list = []
for node in response.nodes:
    if 'ele' in node.tags.keys() and 'name' in node.tags.keys():
        lat = float(node.lat)
        lon = float(node.lon)
        peak_list.append(
            {'elevation':node.tags['ele'],
            'latitude':lat,
            'distance' :distance((lat, lon), (location.raw['lat'], location.raw['lon'])).kilometers,
            'longitude':lon,
            'name':node.tags['name']})

peaks_sorted = sorted(peak_list, key=lambda k: int(k['elevation']))
pprint.pprint(peaks_sorted)
