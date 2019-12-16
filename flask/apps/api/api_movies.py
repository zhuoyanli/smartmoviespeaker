from apps.api import bp
from apps.api.auth import auth_parameters, page_unauth
from flask import request
from pylib.ims import cinema_querier, movie_querier
from pylib import config
from pylib.util import jsonify_list, match_string_lists
from pylib.meta.cinema import CINEMA_IDS

PARAM_CINEMA_ID="cinema_id"
PARAM_CINEMA_KEYWORDS="cinema_keywords"

@bp.route('/movies', methods=['GET'])
def get_movie():
    args = request.args
    #print (args)
    if not auth_parameters(**args):
        return page_unauth(**args)

    if PARAM_CINEMA_KEYWORDS in args:
        # search by keywords
        cinema_keywords = args['cinema_keywords'].split(' ')
        cinema_matched = None
        cinemas = cinema_querier.cinema_by_city_id(config.DEFAULT_CITY_ID)
        for c in cinemas:
            cinema_name_chunks = c.name.split(' ')
            matched_count = match_string_lists(cinema_keywords, cinema_name_chunks)
            if matched_count == 1 and len(cinema_name_chunks) == 1 and len(cinema_keywords) == 1:
                cinema_matched = c
                break
            elif matched_count == 2:
                cinema_matched = c
                break
        if cinema_matched is None:
            return ""
        movies = movie_querier.movie_by_cinema_id(cinema_matched.id)
        return jsonify_list(movies)
    
    if PARAM_CINEMA_ID not in args:
            return "<html>movies api</html>"
        
    movies = movie_querier.movie_by_cinema_id(args[PARAM_CINEMA_ID])
    return jsonify_list(movies)

