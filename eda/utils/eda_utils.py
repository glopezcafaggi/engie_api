import pandas as pd

def get_data_dict(name_list: list) -> dict:
    """Reads data from raw directory and returns {index: dataframe}."""

    def read_data(name):
        return pd.read_csv(
            f"../data/raw/{name}.csv",
            delimiter=",",
            index_col="Date_time"
        )

    return {i: read_data(name_list[i]) for i in range(len(name_list))}