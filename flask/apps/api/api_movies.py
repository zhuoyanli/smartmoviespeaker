from apps.api import bp
from apps.api.auth import auth_parameters, page_unauth
from flask import request
from pylib.ims import movie_querier
from pylib import config
from pylib.util import jsonify_list

PARAM_CINEMA_ID="cinema_id"

@bp.route('/movies', methods=['GET'])
def get_movie():
    args = request.args
    #print (args)
    if not auth_parameters(**args):
        return page_unauth(**args)

    if PARAM_CINEMA_ID not in args:
            return "<html>movies api</html>"
        
    movies = movie_querier.movie_by_cinema_id(args[PARAM_CINEMA_ID])
    return jsonify_list(movies)

