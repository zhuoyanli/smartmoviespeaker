from __future__ import print_function
import json

class Ticket:
    def __init__(self, cinema_name, movie_name, showtime, index_info=None):
        self._cinema_name = cinema_name
        self._movie_name = movie_name
        self._showtime = showtime
        if index_info is None:
            self._idx_info = (0,1)
        else:
            self._idx_info = index_info

    @property
    def index(self):
        return self._idx_info[0]

    @property
    def max_count(self):
        return self._idx_info[1]
            
    def to_json(self):
        json_obj = dict()
        json_obj['cinema'] = self._cinema_name
        json_obj['movie'] = self._movie_name
        json_obj['showtime'] = self._showtime.start_time.short_str()
        json_obj['index'] = "{} of {}".format(self._idx_info[0]+1, self._idx_info[1])
        return json.dumps(json_obj, ensure_ascii=False)

    @classmethod
    def copy_ticket(cls, ticket, index):
        if index >= ticket._idx_info[1]:
            raise ValueError("Out of maximum ticket count: {} for {}".format(index+1, ticket._idx_info[1]))
        new_idx_info = (index, ticket._idx_info[1])
        return Ticket(ticket._cinema_name, ticket._movie_name, ticket._showtime, new_idx_info)
                        
