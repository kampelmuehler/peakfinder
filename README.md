# peakfinder
Tool to find peaks within a specified radius of an address.

### usage example

    $ python3 peakfinder.py -h
    usage: peakfinder.py [-h] [-r RADIUS] [-n COUNT] [-s {elevation,distance}]
                         [-i]
                         address

    Find peaks within some radius around an address.

    positional arguments:
      address               target address

    optional arguments:
      -h, --help            show this help message and exit
      -r RADIUS             radius around address, default: 10
      -n COUNT              number of results to show, 0 gives all (default)
      -s {elevation,distance}
                            key for sorting results
      -i                    invert sorting
    
    $ python3 peakfinder.py "hauptplatz 1 graz" -n 3
    #1      Rannachbauerkogel       ele:842m        dist:9.891km    lat:47.155   lon:15.399
    #2      Marxenkogel             ele:811m        dist:9.475km    lat:47.151   lon:15.400
    #3      Plabutsch               ele:763m        dist:4.602km    lat:47.090   lon:15.385
    
    $ python3 peakfinder.py "hauptplatz 1 graz" -r 0.7
    #1      Schloßberg      ele:475m        dist:0.681km    lat:47.077      lon:15.438
    $ python3 peakfinder.py "hauptplatz 1 graz" -n 3 -i -s distance
