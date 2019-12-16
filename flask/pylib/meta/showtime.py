from __future__ import print_function
import sys
import six
import re

class DateTime:
    PTN_DATETIME = re.compile(r'(?P<y>\d+)-(?P<mon>\d+)-(?P<d>\d+)T(?P<h>\d+):(?P<min>\d+):(?P<s>\d+)(?P<z>[+-].*)')
    DEFAULT_STRING = "2019-12-16T00:00:00-05:00"
    def __init__(self, y, mon, d, h, min, s, z):
        self._year = y
        self._month = mon
        self._dom = d
        self._hour = h
        self._minute = min
        self._second = s
        self._timezone = z

    def __str__(self):
        return "{}-{}-{}:{}:{}:{}".format(self._year, self._month, self._dom,
                                          self._hour, self._minute, self._second)
        
    @classmethod
    def from_string(cls, string):
        m = None
        try:
            #print(string)
            m = cls.PTN_DATETIME.match(string)
        except:
            m = cls.PTN_DATETIME.match(cls.DEFAULT_STRING)

        return DateTime(m.group('y'), m.group('mon'), m.group('d'),
                        m.group('h'), m.group('min'), m.group('s'),
                        m.group('z'))
        
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
