from apps.api import bp
from apps.api.auth import auth_parameters, page_unauth
from pylib.ims import showtime_querier
from pylib.util import jsonify_list
from flask import request

PARAM_CINEMA_ID = "cinema_id"
PARAM_MOVIE_ID = "movie_id"

@bp.route('/showtimes', methods=['GET'])
def get_showtime():
    args = request.args
    #print (args)
    if not auth_parameters(**args):
        return page_unauth(**args)

        if PARAM_CINEMA_ID not in args or PARAM_MOVIE_ID not in args:
            return "<html>showtimes api</html>"
        
    showtimes = showtime_querier.showtime_by_cinema_movie_id(args[PARAM_CINEMA_ID], args[PARAM_MOVIE_ID])
    return jsonify_list(showtimes)

