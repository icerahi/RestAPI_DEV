import json 


def is_valid(json_data):
    try:
        real_json = json.loads(json_data)
        is_valid = True 
    except ValueError:
        is_valid = False 
    return is_valid