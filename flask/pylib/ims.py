from __future__ import print_function
import sys
import json
import urllib
import six
import requests
from . import config
from .meta.city import cities, get_greater_cities
from .meta.movie import Movie
from .meta.cinema import Cinema
from .meta.showtime import Showtime, DateTime
from .meta.ticket import Ticket
from flask import json

_API_KEY = "awsSBNMGASTm03bK4j1r6rFI7Yu3DAyA"
_URL_BASE='https://api.internationalshowtimes.com/v4'

class IMSQuerier:
    def __init__(self, url_base=None, domain=None, api_key=None, **params):
        if not url_base:
            self._url_base = _URL_BASE
        else:
            self._url_base = url_base
        self._domain = domain
        if not api_key:
            self._api_key = _API_KEY
        else:
            self._api_key = api_key
        self._params = params

    @classmethod
    def dict_to_req_params(cls, dict_param):
        req_params = ''
        if dict_param:
            param_strs = []
            for key, value in six.iteritems(dict_param):
                param_strs.append("{}={}".format(key, value))
            req_params += "&".join(param_strs)
        return req_params
        
    def get_url(self, **params):
        url = "{}/{}/?apikey={}".format(self._url_base, self._domain, self._api_key)
        req_param = self.dict_to_req_params(self._params)
        if req_param:
            url += '&'
            url += req_param
        req_param = self.dict_to_req_params(params)
        if req_param:
            url += '&'
            url += req_param
        return url

    def do_query(self, query):
        resp = requests.get(query)
        return resp.json()

class IMSMovieQuerier(IMSQuerier):
    def __init__(self, **params):
        IMSQuerier.__init__(self, domain='movies', **params)

    def _by_city(self, city=None):
        if not city:
            city = cities[config.DEFAULT_CITY_ID]
        return self._by_city_id(city.id)
        
    def _by_city_id(self, city_id=None):
        if not city_id:
            city_id = config.DEFAULT_CITY_ID
        query = self.get_url(city_id=city_id)
        return self.do_query(query)

    def _by_cinema(self, cinema=None):
        if cinema is None:
            return self.by_cinema_id(config.DEFAULT_CINEMA_ID)
        else:
            return self.by_cinema_id(cinema.id)

    def _by_cinema_id(self, cinema_id=None):
        if cinema_id is None:
            cinema_id = config.DEFAULT_CINEMA_ID
        query = self.get_url(cinema_id=cinema_id)
        return self.do_query(query)

    def _movie_from_response(self, req_response):
        for e in req_response['movies']:
            if not e['title']:
                continue
            yield Movie(e['id'], e['title'])

    def movie_by_city_id(self, city_id=None):
        return self._movie_from_response(self._by_city_id(city_id))

    def movie_by_cinema_id(self, cinema_id=None):
        return self._movie_from_response(self._by_cinema_id(cinema_id))
            
movie_querier = IMSMovieQuerier()

        
class IMSCinemaQuerier(IMSQuerier):
    def __init__(self, **params):
        IMSQuerier.__init__(self, domain='cinemas', **params)

    def _by_city_id(self, city_id=None):
        if not city_id:
            city_id = config.DEFAULT_CITY_ID
        query = self.get_url(city_id=city_id)
        return self.do_query(query)

    def _by_loc_dist(self, location, distance):
        query = self.get_url(location=location, distance=distance)
        return self.do_query(query)

    def _cinema_from_response(self, req_response):
        for e in req_response['cinemas']:
            cinema = Cinema.from_json(e)
            yield cinema

    def cinema_by_city_id(self, city_id=None):
        if city_id is None:
            city_id = config.DEFAULT_CITY_ID
        cinemas = []
        gcs = get_greater_cities(city_id)
        if gcs:
            #print("Including greater city members")
            for gc_member in gcs:
                cinemas.extend([c for c in self._cinema_from_response(self._by_city_id(gc_member))])
        else:
            cinemas.extend([c for c in self._cinema_from_response(self._by_city_id(city_id))])
        return cinemas
            
    def cinema_by_loc_dist(self, location, distance):
        return self._cinema_from_response(self._by_loc_dist(location, distance))
            
cinema_querier = IMSCinemaQuerier()


class IMSShowtimeQuerier(IMSQuerier):
    def __init__(self, **params):
        IMSQuerier.__init__(self, domain='showtimes', **params)

    def _by_city_movie_id(self, city_id=None, movie_id=None):
        if not movie_id:
            movie_id = config.DEFAULT_MOVIE_ID
        if city_id is None:
            city_id = config.DEFAULT_CITY_ID
        query = self.get_url(city_id=city_id, movie_id=movie_id)
        return self.do_query(query)

    def _by_cinema_movie_id(self, cinema_id=None, movie_id=None):
        if not movie_id:
            movie_id = config.DEFAULT_MOVIE_ID
        if not cinema_id:
            cinema_id = config.DEFAULT_CINEMA_ID
        query = self.get_url(cinema_id=cinema_id, movie_id=movie_id)
        return self.do_query(query)

    def _showtime_from_response(self, req_response):
        for e in req_response['showtimes']:
            yield Showtime(e['cinema_id'], e['movie_id'], e['start_at'])

    def showtime_by_city_movie_id(self, city_id=None, movie_id=None):
        if city_id is None:
            city_id = config.DEFAULT_CITY_ID

        showtimes = []
        gcs = get_greater_cities(city_id)
        if gcs:
            #print("Including greater city members")
            for gc_member in gcs:
                showtimes.extend([c for c in self._showtime_from_response(self._by_city_movie_id(gc_member, movie_id))])
        else:
            showtimes.extend([c for c in self._showtime_from_response(self._by_city_movie_id(city_id, movie_id))])
        return showtimes

    def showtime_by_cinema_movie_id(self, cinema_id=None, movie_id=None):
        return self._showtime_from_response(self._by_cinema_movie_id(cinema_id, movie_id))
    
showtime_querier = IMSShowtimeQuerier()

class IMSTicketQuerier(IMSQuerier):
    def __init__(self, **params):
        IMSQuerier.__init__(self, domain='tickets', **params)

    def ticket_by_city_cinema_movie(self, city_id=None, cinema_id=None, movie_id=None, count=None):
        cinema_name = ""
        cinemas = cinema_querier.cinema_by_city_id(city_id)
        for c in cinemas:
            if c.id == cinema_id:
                cinema_name = c.name
                break
        movies = movie_querier.movie_by_cinema_id(cinema_id)
        for m in movies:
            if m.id == movie_id:
                movie_name = m.title
                break

        showtime = None
        for st in showtime_querier.showtime_by_cinema_movie_id(cinema_id, movie_id):
            showtime = st
            break
        if count is None:
            index_info = (0,1)
        else:
            index_info = (0, count)
        return Ticket(cinema_name, movie_name, showtime, index_info)
        
        
    def ticket_by_city_cinema_movie_starttime(self, city_id=None, cinema_id=None, movie_id=None, target_start_time=None, count=None):
        cinema_name = ""
        cinemas = cinema_querier.cinema_by_city_id(city_id)
        for c in cinemas:
            if c.id == cinema_id:
                cinema_name = c.name
                break
        movies = movie_querier.movie_by_cinema_id(cinema_id)
        for m in movies:
            if m.id == movie_id:
                movie_name = m.title
                break
        showtime = None
        target_starttime_obj = DateTime.from_string(target_start_time)
        for st in showtime_querier.showtime_by_cinema_movie_id(cinema_id, movie_id):
            if target_starttime_obj > st.start_time:
                continue
            showtime = st
            break
        if count is None:
            index_info = (0,1)
        else:
            index_info = (0, count)
        return Ticket(cinema_name, movie_name, showtime, index_info)
        
ticket_querier = IMSTicketQuerier()
