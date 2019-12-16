from apps.api import bp
from apps.api.auth import auth_parameters, page_unauth
from pylib.ims import cinema_querier
from flask import Flask, request

@bp.route('/cinemas', methods=['GET'])
def get_cinema():
    args = request.args
    #print (args)
    if not auth_parameters(**args):
        return page_unauth(**args)
        
    return "<html>cinema api</html>"
