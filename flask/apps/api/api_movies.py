from apps.api import bp
from apps.api.auth import auth_parameters, page_unauth
from flask import request
from pylib.ims import movie_querier
from pylib import config

@bp.route('/movies', methods=['GET'])
def get_movie():
    args = request.args
    #print (args)
    if not auth_parameters(**args):
        return page_unauth(**args)

    return "<html>movies api</html>"
