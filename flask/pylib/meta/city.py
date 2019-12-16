import json
import six
from .us_cities import US_CITIES

# Seattle, Bellevue, Everett, Tacoma
list_greater_cities = [ [ "4966", "4947", "4969", "20184" ]]


class City:
    def __init__(self, id, name):
        self._id = id
        self._name = name
        
    @property
    def id(self):
        return self._id
    def __str__(self):
        return self._name
    def __repr__(self):
        return self._name
    

json_cities = json.loads(US_CITIES)
cities = dict()

for id, name in six.iteritems(json_cities):
    cities[id] = City(id, name)

_greater_cities = list()
for gc in list_greater_cities:
    _greater_cities.append(set(gc))

def get_greater_cities(city_id):
    for gc in _greater_cities:
        if city_id in gc:
            return gc
    return None
