import json

def read_json(file):
    f=open(file)
    data=json.load(f)
    f.close()
    return data

def write_json(file, data):
    f=open(file,"w")
    json_data=json.dumps(data, indent=4)
    f.write(json_data)
    f.close()