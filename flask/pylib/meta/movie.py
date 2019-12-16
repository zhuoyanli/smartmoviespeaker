import json

class Movie:
    def __init__(self, id, title):
        self._id = id
        self._title = title

    @classmethod
    def from_json(self, json_string):
        json_obj = json.loads(json_string)
        return Movie(json_obj['id'], json_obj['title'])

    @classmethod
    def from_dict(self, dict_data):
        return Movie(dict_data['id'], dict_data['title'])

    def to_json(self):
        dict_data = dict()
        dict_data['id'] = self._id
        dict_data['title'] = self._title
        return json.dumps(dict_data)

    @property
    def id(self):
        return self._id

    @property
    def title(self):
        return self._title

    def __str__(self):
        return "id: {} title: {}".format(self._id, self._title)

    def __repr__(self):
        return self._title
