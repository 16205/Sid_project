import json
import numpy as np 

def buildJson(folder_name, name, data):
    file_name = folder_name+'/'+name+'.json'
    print(file_name)
    with open(file_name, 'w') as file:
        json.dump(data, file, indent = 4)

def getJsonData(json_name):
    with open(json_name, 'r') as file:
        data =  json.load(file)
    return data

def serializeVectorList(vector_list):
    serialized_list = []
    for vector in vector_list:
            x, y, z = vector[0], vector[1], vector[2]
            serialized_list.append([x, y, z])  
    return serialized_list