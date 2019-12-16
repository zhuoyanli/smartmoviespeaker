import re
from apps.api import bp
from apps.api.auth import auth_parameters, page_unauth
from pylib import config
from pylib.ims import cinema_querier, movie_querier, showtime_querier
from pylib.util import jsonify_list, match_string_lists
from flask import request

PARAM_CINEMA_ID = "cinema_id"
PARAM_MOVIE_ID = "movie_id"
PARAM_CINEMA_KEYWORDS = "cinema_keywords"
PARAM_MOVIE_KEYWORDS = "movie_keywords"

@bp.route('/showtimes', methods=['GET'])
def get_showtime():
    args = request.args
    #print (args)
    if not auth_parameters(**args):
        return page_unauth(**args)

    if PARAM_CINEMA_KEYWORDS in args:
        # search by keywords
        cinema_keywords = args[PARAM_CINEMA_KEYWORDS].split(' ')
        cinema_matched = None
        cinemas = cinema_querier.cinema_by_city_id(config.DEFAULT_CITY_ID)
        for c in cinemas:
            cinema_name_chunks = c.name.split(' ')
            matched_count = match_string_lists(cinema_keywords, cinema_name_chunks)
            if matched_count == 1 and len(cinema_name_chunks) == 1 and len(cinema_keywords) == 1:
                cinema_matched = c
                break
            elif matched_count >= 2:
                cinema_matched = c
                break
        if cinema_matched is None:
            return ""
        
        movie_keywords = args[PARAM_MOVIE_KEYWORDS].split(' ')
        movie_matched = None
        movies = movie_querier.movie_by_cinema_id(cinema_matched.id)
        for m in movies:
            m_title_c = re.sub(r'[:\-()]', '', m.title)
            movie_title_chunks = m_title_c.split(' ')
            matched_count = match_string_lists(movie_keywords, movie_title_chunks)
            if matched_count == 1 and len(movie_title_chunks) == 1 and len(movie_keywords) == 1:
                movie_matched = m
                break
            elif matched_count >= 2:
                movie_matched = m
                break
        if movie_matched is None:
            return ""
        
        showtimes = showtime_querier.showtime_by_cinema_movie_id(cinema_matched.id, movie_matched.id)
        return jsonify_list(showtimes)
    
    
    if PARAM_CINEMA_ID not in args or PARAM_MOVIE_ID not in args:
        return "<html>showtimes api</html>"
        
    showtimes = showtime_querier.showtime_by_cinema_movie_id(args[PARAM_CINEMA_ID], args[PARAM_MOVIE_ID])
    return jsonify_list(showtimes)

