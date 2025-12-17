import numpy as np
import pandas as pd

from keras.models import load_model

def df_to_X_y(data, window_size=2):
    df_as_np = data.to_numpy()
    X = []
    y = []
    for i in range(len(df_as_np)-window_size):
        row = [r for r in df_as_np[i:i+window_size]]
        X.append(row)
        label = df_as_np[i+window_size][-1]
        y.append(label)
    return np.array(X), np.array(y)
    
def add_yearly_fourier(df): 
    ts = pd.to_datetime(df.index) 
    day_of_year = ts.dayofyear 
    T = 365.25 
    df = df.copy() 
    df["year_sin"] = np.sin(2 * np.pi * day_of_year / T) 
    df["year_cos"] = np.cos(2 * np.pi * day_of_year / T) 
    return df 

def encode_wind_direction_circular(df): 
    df = df.copy() 
    theta = np.deg2rad(df["wind_deg"] % 360) 
    df["wind_sin"] = np.sin(theta) 
    df["wind_cos"] = np.cos(theta)
    df.drop(columns=["wind_deg"], inplace=True) 
    return df 

def feature_pipeline(df):
    if 'P_avg' in df.columns:
        df_X = df.drop(columns=['P_avg'])
        df_y = df['P_avg']
        df_X = encode_wind_direction_circular(df_X) 
        df_X = add_yearly_fourier(df_X) 
        df = pd.concat([df_X, df_y], axis=1)
        return df
    
    else:
        df = encode_wind_direction_circular(df) 
        df = add_yearly_fourier(df) 
        return df

def predictions(data, model):
    #model = load_model('../models/model1.keras')
    data_ml = feature_pipeline(data)
    X  = df_to_X_y(data_ml)[0]
    array = model.predict(X).ravel()
    data_pred = pd.DataFrame({'P_avg_predictions': array})
    return data_pred