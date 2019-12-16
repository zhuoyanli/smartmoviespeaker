from flask import Blueprint

bp = Blueprint('api', __name__)

from apps.api import api_movies, api_cinemas, api_showtimes, api_tickets


