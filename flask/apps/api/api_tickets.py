import six
import re
from apps.api import bp
from apps.api.auth import auth_parameters, page_unauth
from pylib.util import jsonify_list, match_string_lists
from pylib import config
from pylib.ims import cinema_querier, movie_querier, showtime_querier, ticket_querier
from pylib.meta.ticket import Ticket
from flask import request


PARAM_CITY_ID = "city_id"
PARAM_CINEMA_ID = "cinema_id"
PARAM_MOVIE_ID = "movie_id"
PARAM_STARTTIME = "start_time"
PARAM_TICKET_COUNT = "count"
PARAM_CINEMA_KEYWORDS = "cinema_keywords"
PARAM_MOVIE_KEYWORDS = "movie_keywords"


@bp.route('/tickets', methods=['GET'])
def get_ticket():
    args = request.args
    if not auth_parameters(**args):
        return page_unauth(**args)

    count = None
    if PARAM_TICKET_COUNT in args:
        count = int(args[PARAM_TICKET_COUNT])

    city_id = config.DEFAULT_CITY_ID
    if city_id in args:
        city_id = args[PARAM_CITY_ID]
        
    cinema_matched = None
    if PARAM_CINEMA_KEYWORDS in args:
        # search by keywords
        cinema_keywords = args[PARAM_CINEMA_KEYWORDS].split(' ')
        cinema_matched = None
        cinemas = cinema_querier.cinema_by_city_id(city_id)
        for c in cinemas:
            cinema_name_chunks = c.name.split(' ')
            matched_count = match_string_lists(cinema_keywords, cinema_name_chunks)
            if matched_count == 1 and len(cinema_name_chunks) == 1 and len(cinema_keywords) == 1:
                cinema_matched = c
                break
            elif matched_count >= 2:
                cinema_matched = c
                break
        if cinema_matched is None:
            return ""

    movie_matched = None
    if PARAM_MOVIE_KEYWORDS in args:
        movie_keywords = args[PARAM_MOVIE_KEYWORDS].split(' ')
        movie_matched = None
        movies = movie_querier.movie_by_cinema_id(cinema_matched.id)
        for m in movies:
            m_title_c = re.sub(r'[:\-()]', '', m.title)
            movie_title_chunks = m_title_c.split(' ')
            matched_count = match_string_lists(movie_keywords, movie_title_chunks)
            if matched_count == 1 and len(movie_title_chunks) == 1 and len(movie_keywords) == 1:
                movie_matched = m
                break
            elif matched_count >= 2:
                movie_matched = m
                break
        if movie_matched is None:
            return ""

        if cinema_matched:
            ticket = ticket_querier.ticket_by_city_cinema_movie(city_id,
                                                                cinema_matched.id,
                                                                movie_matched.id,
                                                                count)
            if count is None:
                count =1 
            tickets = []
            tickets.append(ticket)

            if PARAM_TICKET_COUNT in args and count > 1:
                for idx in range(2, count+1):
                    tickets.append(Ticket.copy_ticket(ticket, idx-1))
            return jsonify_list(tickets)
            
    if PARAM_CINEMA_ID not in args or PARAM_MOVIE_ID not in args or PARAM_STARTTIME not in args:
        return "<html>tickets api</html>"

    city_id = config.DEFAULT_CITY_ID
    if PARAM_CITY_ID in args:
        city_id = args[PARAM_CITY_ID]

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
