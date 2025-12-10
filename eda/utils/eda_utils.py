import pandas as pd
import numpy as np 

def get_data_dict(name_list: list) -> dict:
    """Reads data from raw directory and returns {index: dataframe}."""

    def read_data(name):
        return pd.read_csv(
            f"../data/raw/{name}.csv"
            , delimiter=","
            #, index_col="Date_time"
        )

    return {i: read_data(name_list[i]) for i in range(len(name_list))}


def give_time_interval(data):
    col =  data['Date_time_nr'] 
    return display("end:", col.max(), "start:+", col.min(), "entries:", col.shape)

def give_time_discrepancies(data):
    time =  data['Date_time_nr'] 
    return time.diff().unique()

def preprocess(data):
    # useless cols
    data = data.drop(columns=['Date_time', 'Wind_turbine_name'])
    #set datetime unix format as timestap
    data = data.set_index('Date_time_nr')

    # create index array    
    end = 1515798000
    start = 1356994800
    period = 600 
    periods_timedelta =  (end - start)/period
    index_array = np.arange(int(periods_timedelta)+1) * period + start
    
    for idx in index_array:
        if idx not in data.index:
        # start with all NaNs
            data.loc[idx] = {col: pd.NA for col in data.columns}
        
    # ensure sorted index if needed
    data.sort_index(inplace=True)

    #fill-in nans
    data.ffill(inplace=True)

    return data 