import pandas as pd



### read mock data
def read_all_json():
    data_dic = {i:  pd.read_json(f'data/json/jdata{i}.json', orient='split')  for i in range(1,5)}
    return data_dic

def read_one_json(id):
    data = pd.read_json(f'data/json/jdata{id}.json', orient='split')  
    return data


