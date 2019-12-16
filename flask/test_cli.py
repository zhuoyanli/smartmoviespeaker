from __future__ import print_function
import sys
import argparse
from pylib.ticket import TicketService
from pylib.ims import movie_querier, cinema_querier, showtime_querier
from pylib import config
from pylib.meta.cinema import Cinema
from pylib.meta.showtime import DateTime
from flask import json

def test_ims(*args):
    parser = argparse.ArgumentParser()
    parser.add_argument("--app", "-a", required=True)
    parser.add_argument("--city", "-c")
    parser.add_argument("--cinema" "-t")
    args = parser.parse_args(*args)

    if args.app == "movie":
        #resp = movie_querier.by_city()
        #print(resp)
        for m in movie_querier.movie_by_city_id("5088"):
        #for m in movie_querier.movie_from_response(resp):
            print(m)
    elif args.app == "cinema":
        #resp = cinema_querier.by_city()
        #for c in  cinema_querier.cinema_by_loc_dist(location=config.DEFAULT_LOCATION, distance=50):
        #for c in cinema_querier.cinema_by_city_id("5088"):
        #print(c)
        cinemas = cinema_querier.cinema_by_city_id("5088")
        print(json.dumps(cinemas, ensure_ascii=False))
    elif args.app == 'showtime':
        #for s in showtime_querier.showtime_by_city_movie_id("5088", "25536"):
        for s in showtime_querier.showtime_by_cinema_movie_id("48105", "25536"):
            print(s)
        #dt = DateTime.from_string("2019-12-19T21:45:00-05:00")

    
        
module = sys.argv[1]

if module == 'ims':
    print(sys.argv[2:])
    test_ims(sys.argv[2:])
