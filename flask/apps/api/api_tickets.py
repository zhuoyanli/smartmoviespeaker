from apps.api import bp
from apps.api.auth import auth_parameters, page_unauth
from pylib.ims import ticket_querier
from flask import request

@bp.route('/tickets', methods=['GET'])
def get_ticket():
    args = request.args
    if not auth_parameters(**args):
        return page_unauth(**args)

    return "<html>tickets api</html>"
