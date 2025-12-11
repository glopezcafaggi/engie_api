
import numpy as np 
import pandas as pd 
from sklearn.decomposition import PCA

from sklearn.preprocessing import StandardScaler
from sklearn.preprocessing import MinMaxScaler
from sklearn.preprocessing import RobustScaler

from sklearn.decomposition import PCA


def ML_scaler(data, scaler=None):
    if scaler == None:
        return data

    cols = data.columns
    index = data.index
    data_sc = pd.DataFrame(data =  scaler.fit_transform(data), columns=cols, index=index)
    
    return data_sc

def ML_pca(data, n_components=2):
    pca = PCA(n_components=n_components) 
    X = data.drop(columns=['P_avg'])
    cols = X.columns
    index = data.index
    data_sc = pd.DataFrame(data =  pca.fit_transform(X), index=index)
    data_sc['P_avg'] = data['P_avg'] 
    return data_sc

def add_yearly_fourier(df):
    # timestamps as date
    ts = pd.to_datetime(df.index, unit='s')

    # Day of year (1..365 or 366 for leap)
    day_of_year = ts.dayofyear

    # Period T = 365 days (approx yearly cycle)
    T = 365

    # Add Fourier components
    df["year_sin"] = np.sin(2 * np.pi * day_of_year / T)
    df["year_cos"] = np.cos(2 * np.pi * day_of_year / T)

    return df


def encode_wind_direction_circular(df):
    """
    Add smooth circular (sin/cos) encoding for wind direction in degrees (0–360).
    """
    # Normalize angle to 0–360
    theta = np.deg2rad(df['wind_deg'] % 360)

    df["wind_sin"] = np.sin(theta)
    df["wind_cos"] = np.cos(theta)
    df.drop(columns=['wind_deg'], inplace=True)

    return df


###pipelines
def pipeline_train(data, scaler):
    data_ml = data.drop(columns=['P_avg', "wind_deg"])
    data_ml = ML_scaler(data_ml, scaler)
    data_ml["wind_deg"] = data["wind_deg"]
    data_ml = encode_wind_direction_circular(data_ml)
    data_ml = add_yearly_fourier(data_ml)

    # reoder cols
    
    data_ml['P_avg'] = data['P_avg']
    return data_ml

def pipeline_predict(data, scaler):
    data_ml = data.drop(columns=[ "wind_deg"])
    data_ml = ML_scaler(data_ml, scaler)
    data_ml["wind_deg"] = data["wind_deg"]
    data_ml = encode_wind_direction_circular(data_ml)
    data_ml = add_yearly_fourier(data_ml)

    return data_ml


#### lag featuring

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

def df_to_X(data, window_size=2):
    df_as_np = data.to_numpy()
    X = []
    for i in range(len(df_as_np)-window_size):
        row = [r for r in df_as_np[i:i+window_size]]
        X.append(row)
    return np.array(X)

# predict sequence from data clean
def predict(data, model):
    MM_scaler = MinMaxScaler()
    

    data_ml = pipeline_predict(data,  MM_scaler)
    X = df_to_X(data_ml)
    predictions = model.predict(X)
    data = pd.DataFrame(data=predictions, columns=['P_avg_pred'])
    return data