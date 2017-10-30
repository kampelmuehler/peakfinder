#!/usr/bin/env python3

__author__ = "Moritz Kampelmuehler"

import argparse
import dill as pickle
from geopy.geocoders import Nominatim
from geopy.distance import vincenty as distance
import overpy
import os
import os.path

def main():
    parser = argparse.ArgumentParser(
            description='Find peaks within some radius around an address.')
    parser.add_argument(dest='address', type=str, help='target address')
    parser.add_argument('-r', dest='radius', type=float, default=10.,
            help='radius around address, default: 10')
    parser.add_argument('-n', dest='count', type=int, default=0,
            help='number of results to show, 0 gives all (default)')
    parser.add_argument('-s', dest='sort_key', type=str,
            choices=['elevation', 'distance'], default='elevation',
            help='key for sorting results')
    parser.add_argument('-i', dest='sort_inv', action='store_true',
            default=False, help='invert sorting')

    args = parser.parse_args()

    address, radius, count = args.address, args.radius, args.count
    sort_key, sort_inv = args.sort_key, args.sort_inv

    assert(sort_key in ['distance', 'elevation'])
    assert(type(count) is int)
    assert(type(radius) is float)
    assert(count >= 0)

    geolocator = Nominatim()
    location = geolocator.geocode(address, addressdetails=True)

    cachedir = os.path.join(os.path.expanduser('~'), '.peakfinder_cache')

    if not os.path.exists(cachedir):
      os.mkdir(cachedir)

    address_formatted = "".join(c.lower() for c in address if c.isalnum())
    filename = "data_{0:s}_{1:g}.pkl".format(address_formatted, int(radius))
    filepath = os.path.join(cachedir, filename)

    radius *= 1e3

    if not os.path.isfile(filepath):
        api = overpy.Overpass()
        response = api.query("""
            node[natural=peak](around:{}, {}, {});
            out;
            """.format(radius, location.raw['lat'], location.raw['lon']))

        with open(filepath, 'wb') as f:
            pickle.dump(response, f)
    else:
        with open(filepath, 'rb') as f:
            response = pickle.load(f)

    peak_list = []
    for node in response.nodes:
        if 'ele' in node.tags.keys() and 'name' in node.tags.keys():
            lat = float(node.lat)
            lon = float(node.lon)
            dist = distance((lat, lon), (location.raw['lat'], location.raw['lon']))
            peak_list.append(
                {'elevation': node.tags['ele'],
                'latitude': lat,
                'distance': dist.kilometers,
                'longitude': lon,
                'name': node.tags['name']})

    if not peak_list:
        return

    peaks_sorted = sorted(peak_list, key=lambda k: int(k[sort_key]))

    peaks_print = peaks_sorted if sort_inv else peaks_sorted[::-1]
    peaks_print = peaks_print if count == 0 else peaks_print[:count]

    name_width = max([len(peak['name']) for peak in peaks_print])
    format_str = ('#{0:d}\t{1:' + str(name_width) + 's}\tele:{2:d}m\t'
            'dist:{3:.3f}km\tlat:{4:.3f}\tlon:{5:.3f}')

    for k, peak in enumerate(peaks_print):
        name, dist = peak['name'], peak['distance']
        lat, lon = peak['latitude'], peak['longitude']
        elev = int(peak['elevation'])

        print(format_str.format(k+1, name, elev, dist, lat, lon))

if __name__ == '__main__':
    main()
