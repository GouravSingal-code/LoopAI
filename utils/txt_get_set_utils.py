
import json,os

def set_txt(data,location):
    with open(location, 'w') as file:
        json.dump(data, file)

def get_txt(location):
    with open(location) as json_file:
        data = json.load(json_file)
    return data

