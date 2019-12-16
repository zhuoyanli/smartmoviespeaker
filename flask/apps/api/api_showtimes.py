from apps.api import bp
from apps.api.auth import auth_parameters, page_unauth
from pylib.ims import showtime_querier
from flask import request

@bp.route('/showtimes', methods=['GET'])
def get_showtime():
    args = request.args
    #print (args)
    if not auth_parameters(**args):
        return page_unauth(**args)

    return "<html>showtimes api</html>"
