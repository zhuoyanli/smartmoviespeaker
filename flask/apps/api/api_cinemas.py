from apps.api import bp
from apps.api.auth import auth_parameters, page_unauth
from pylib.ims import cinema_querier
from pylib.util import jsonify_list
from pylib import config
from flask import Flask, request, jsonify
from pylib.meta.cinema import CINEMA_IDS

PARAM_CITY_ID = 'city_id'

@bp.route('/cinemas', methods=['GET'])
def get_cinema():
    args = request.args
    #print (args)
    if not auth_parameters(**args):
        return page_unauth(**args)

    city_id = config.DEFAULT_CITY_ID
    if PARAM_CITY_ID in args:
        city_id = args['city_id']
    cinemas = cinema_querier.cinema_by_city_id(city_id)
    return jsonify_list(cinemas)
