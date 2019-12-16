from __future__ import print_function
import sys
import six
import re
import json
from functools import total_ordering

@total_ordering
class DateTime:
    PTN_DATETIME = re.compile(r'(?P<y>\d+)-(?P<mon>\d+)-(?P<d>\d+)T(?P<h>\d+):(?P<min>\d+):(?P<s>\d+)(?P<z>[+-].*)')
    DEFAULT_STRING = "2019-12-16T00:00:00-05:00"
    def __init__(self, y, mon, d, h, min, s, z, orig_str):
        self._year = y
        self._month = mon
        self._dom = d
        self._hour = h
        self._minute = min
        self._second = s
        self._timezone = z
        self._orig_str = orig_str

    def __str__(self):
        #return "{}-{}-{}:{}:{}:{}".format(self._year, self._month, self._dom,
        #                                  self._hour, self._minute, self._second)
        return self._orig_str

    def short_str(self):
        return "{}-{}-{}:{}:{}".format(self._year, self._month, self._dom,
                                       self._hour, self._minute)
    
    def __eq__(self, other):
        if not isinstance(other, DateTime):
            return False
        if self is other:
            return True
        if self._year == other._year and \
           self._month == other._month and \
           self._dom == other._dom and \
           self._hour == other._hour and \
           self._minute == other._minute and \
           self._second == other._second:
            return True
        else:
            return False

    def __ne__(self, other):
        return not self.__eq__(other)
    
    def __lt__(self, other):
        if self.__eq__(other):
            return False
        if isinstance(other, DateTime) is False:
            raise ValueError("Not a DateTime object in __lt__: {}".format(other))
        if other._year > self._year:
            return False
        if self._year > other._year:
            return True
        if other._month > self._month:
            return False
        if self._month > other._month:
            return True
        if other._dom > self._dom:
            return False
        if self._dom > other._dom:
            return True
        if other._hour > self._hour:
            return False
        if self._hour > other._hour:
            return True
        if other._minute > self._minute:
            return False
        if self._minute > other._minute:
            return True

        return False
    
    @classmethod
    def from_string(cls, string):
        m = None
        try:
            #print(string)
            m = cls.PTN_DATETIME.match(string)
        except:
            string = cls.DEFAULT_STRING
            m = cls.PTN_DATETIME.match(string)

        return DateTime(m.group('y'), m.group('mon'), m.group('d'),
                        m.group('h'), m.group('min'), m.group('s'),
                        m.group('z'), string)
        
class Showtime:
    def __init__(self, cinema_id=None, movie_id=None, start_time=None):
        self._cinema_id = cinema_id
        self._movie_id = movie_id
        self._start_time = DateTime.from_string(start_time)

    @property
    def start_time(self):
        return self._start_time

    @property
    def cinema_id(self):
        return self._cinema_id

    @property
    def movie_id(self):
        return self._movie_id

    def __str__(self):
        return "cinema_id: {} movie_id: {} start_time: {}".format(self._cinema_id, self._movie_id, self._start_time)

    def to_json(self):
        json_obj = dict()
        json_obj['cinema_id'] = self._cinema_id
        json_obj['movie_id'] = self._movie_id
        json_obj['start_time'] = str(self._start_time)
        return json.dumps(json_obj, ensure_ascii=False)
