import re
PTN_PUNCT = re.compile(r':-()')

def jsonify_list(lst_tojson):
    json_str = "["
    json_str_col = [ e.to_json() for e in lst_tojson ]
    json_str += ",".join(json_str_col)
    json_str += "]"
    return json_str

def match_string_lists(str_lst1, str_lst2):
    count = 0
    for s1 in str_lst1:
        for s2 in str_lst2:
            if s1.lower() == s2.lower():
                count += 1
    return count
