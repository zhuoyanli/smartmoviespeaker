from __future__ import print_function
import sys
import six
import json

RETURN_CODES_JSON = """{
"SUCCESS": [0, "SUCCESS"],
"ERR_NO_CINEMA_ID": [40001, "Missing cinema ID"],
"ERR_NO_CITY_ID": [40002, "Missing city ID"],
"ERR_NO_MOVIE_ID": [40003, "Missing movie ID"],
"ERR_NO_SHOWTIME": [40004, "Missing showtime"],
"VOID": [-1, "UNDEFINED"]
}
"""

class ReturnValue:
    def __init__(self, code, name, err_str):
        self._code = code
        self._err_str = err_str

json_codes = json.loads(RETURN_CODES_JSON)

return_codes = dict()
registered_values = dict()

for code_name, code_attrib in six.iteritems(json_codes):
    if code_attrib[0] in registered_values:
        raise Exception("Return code already registered: existing: {}:{}, incoming: {}:{}".format(code_attrib[0], registered_values[code_attrib[0]],
                                                                                                  code_attrib[0], code_name))
    return_codes[code_name] = ReturnValue(code_attrib[0], code_name, code_attrib[1])
