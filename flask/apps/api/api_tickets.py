import six

from apps.api import bp
from apps.api.auth import auth_parameters, page_unauth
from pylib.util import jsonify_list
from pylib import config
from pylib.ims import ticket_querier
from pylib.meta.ticket import Ticket
from flask import request


PARAM_CITY_ID = "city_id"
PARAM_CINEMA_ID = "cinema_id"
PARAM_MOVIE_ID = "movie_id"
PARAM_STARTTIME = "start_time"
PARAM_TICKET_COUNT = "count"

    
@bp.route('/tickets', methods=['GET'])
def get_ticket():
    args = request.args
    if not auth_parameters(**args):
        return page_unauth(**args)
    if PARAM_CINEMA_ID not in args or PARAM_MOVIE_ID not in args or PARAM_STARTTIME not in args:
        return "<html>tickets api</html>"

    city_id = config.DEFAULT_CITY_ID
    if PARAM_CITY_ID in args:
        city_id = args[PARAM_CITY_ID]

    count = None
    if PARAM_TICKET_COUNT in args:
        count = int(args[PARAM_TICKET_COUNT])
    ticket = ticket_querier.ticket_by_city_cinema_movie_starttime(city_id,
                                                                  args[PARAM_CINEMA_ID],
                                                                  args[PARAM_MOVIE_ID],
                                                                  args[PARAM_STARTTIME],
                                                                  count)
    if count is None:
        count =1 
    tickets = []
    tickets.append(ticket)

    if PARAM_TICKET_COUNT in args and count > 1:
        for idx in range(2, count+1):
            tickets.append(Ticket.copy_ticket(ticket, idx-1))

    return jsonify_list(tickets)
