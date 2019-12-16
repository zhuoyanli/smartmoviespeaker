from __future__ import print_function
import six

class QueryResult:
    def __init__(self, return_code, payload_json=None):
        self._retcode = return_code
        self._payload = payload_json


    
