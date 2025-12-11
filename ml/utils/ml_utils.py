import pandas as pd
import numpy as np

import matplotlib.pyplot as plt


def read_one_df():
    data = pd.read_csv('../data/dataML/data0.csv', index_col='Date_time_nr')
    return data

def read_all_df():
    data_dict = { i : pd.read_csv(f'../data/dataML/data{i}.csv', index_col='Date_time_nr')  for i in range(4)}
    return data_dict

def clean_data(data_raw):
        #drop useless cols
        cols_drop = ['Ws1_avg'
                , 'Ws2_avg'
                , 'Ws_avg'
                , 'Wa_avg'
                , 'Ya_avg'
                , 'Va_avg']
        data = data_raw.drop(columns=cols_drop)
        
        # reaganre variables
        X_var = [ 'temp'
        , 'pressure'
        , 'humidity'
        , 'wind_speed'
        , 'wind_deg'
        , 'rain_1h'
        , 'snow_1h' ]

        Y_var = [ 'P_avg'
        , 'Yt_avg'
        , 'Rs_avg'
        , 'Rbt_avg'
        , 'Rm_avg']

        data = data[X_var+ Y_var] 
        # fix years spans 
        data = data.loc[1356998400: 1514764200]

        return data

def transform_tohourdata(data_clean):
    #data_clean shape (262944, 12) timestamps each 10 min unix
    length = 262944
    entries_per_hour = 6
    array = data_clean.to_numpy()
    array_mean = np.zeros( (int(length / entries_per_hour) , 12))

    for i in range(int(length / entries_per_hour)):
        array_mean[i] = np.sum(array[6*i: 6*i+6], axis=0)/6

    index_array = np.arange(1356998400 ,  1514764800 , 3600 )

    data = pd.DataFrame(data=array_mean
                        , columns=data_clean.columns 
                        , index= index_array)
    return data 

def transform_todailydata(data_clean):
    #data_clean shape (262944, 12) timestamps each 10 min unix
    length = 262944
    entries_per_hour = 6*24
    array = data_clean.to_numpy()
    array_mean = np.zeros( (int(length / entries_per_hour) , 12))

    for i in range(int(length / entries_per_hour)):
        array_mean[i] = np.mean(array[entries_per_hour*i: entries_per_hour*i+entries_per_hour], axis=0)

    index_array = np.arange(1356998400 ,  1514764800 , 60*60*24 )

    data = pd.DataFrame(data=array_mean
                        , columns=data_clean.columns 
                        , index= index_array)
    return data 

def unix_to_dates(data, unit="s"):
    data = data.copy()
    data.index = pd.to_datetime(data.index, unit=unit)
    return data

def plot_power_year(year_datas):
    n = len(year_datas)

    fig, axes = plt.subplots(n, 1, figsize=(12, 3*n))

    for ax, (k, v) in zip(axes, year_datas.items()):
        v.plot(ax=ax)
        ax.set_title(f"Year {k}")

    plt.tight_layout()
    plt.show()

