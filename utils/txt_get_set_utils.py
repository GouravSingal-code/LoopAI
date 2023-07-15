
import json,os

def set_txt(data,location):
    with open(os.path.abspath(location), 'w') as file:
        json.dump(data, file)

def get_txt(location):
    with open(os.path.abspath(location)) as json_file:
        data = json.load(json_file)
    return data

