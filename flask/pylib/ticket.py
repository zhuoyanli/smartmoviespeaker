from __future__ import print_function
import sys
import six
from . import config
from .error import return_codes
from .query import QueryResult

class TicketService:
    DEF_RET_CODE=return_codes['SUCCESS']
    
    def __init__(self, query_handler):
        self._query_handler = query_handler
        
    def check_availability(self, city_id=None, cinema_id=None, movie_id=None, showtime=None):
        ret_code = self.DEF_RET_CODE
        
        if not cinema_id:
            return QueryResult(return_codes['ERR_NO_CINEMA_ID'])
        if not movie_id:
            return QueryResult(return_codes['ERR_NO_MOVIE_ID'])
        if not showtime:
            return QueryResult(return_codes['ERR_NO_SHOWTIME'])
        if not city_id:
            city_id = config.DEFAULT_CITY_ID
