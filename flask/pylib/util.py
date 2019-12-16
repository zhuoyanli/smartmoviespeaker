def jsonify_list(lst_tojson):
    json_str = "["
    json_str_col = [ e.to_json() for e in lst_tojson ]
    json_str += ",".join(json_str_col)
    json_str += "]"
    return json_str
