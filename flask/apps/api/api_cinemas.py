from apps.api import bp
from apps.api.auth import auth_parameters, page_unauth
from pylib.ims import cinema_querier
from pylib.util import jsonify_list
from flask import Flask, request, jsonify

@bp.route('/cinemas', methods=['GET'])
def get_cinema():
    args = request.args
    #print (args)
    if not auth_parameters(**args):
        return page_unauth(**args)

    cinemas = cinema_querier.cinema_by_city_id(args['city_id'])
    return jsonify_list(cinemas)
