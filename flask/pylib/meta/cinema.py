import json
from .city import cities

cinemas = dict()

class Cinema:
    def __init__(self, id, name, city_id, latitude, longitude):
        self._id = id
        self._city_id = city_id
        self._city = cities[city_id]
        self._lat = latitude
        self._long = longitude
        self._name = name
        if id not in cinemas:
            cinemas[id] = self
        
    @classmethod
    def from_json(cls, json_obj):
        return Cinema(json_obj['id'], json_obj['name'], json_obj['city_id'],
                      json_obj['location']['lat'], json_obj['location']['lon'])

    @classmethod
    def from_jsonstring(cls, json_string):
        return cls.from_json(json.loads(json_string))

    @classmethod
    def from_dict(self, dict_data):
        return Cinema(dict_data['id'], dict_data['name'], dict_data['city_id'],
                      dict_data['location']['lat'], dict_data['location']['lon'])

    def to_json(self):
        dict_data = dict()
        dict_data['id'] = self._id
        dict_data['name'] = self._name
        dict_data['city_id'] = self._city.id
        dict_loc = dict()
        dict_loc['lat'] = self._lat
        dict_loc['long'] = self._long
        dict_data['location'] = dict_loc
        return json.dumps(dict_data)

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    @property
    def city(self):
        return self._city

    @property
    def city_id(self):
        return self._city_id

    @property
    def coordinates(self):
        return "{},{}".format(self._lat, self._long)

    def __str__(self):
        return "id: {}, name: {}, city: {} city_id: {}".format(self._id, self._name, self._city, self._city_id)

    def __repr__(self):
        return self._name
