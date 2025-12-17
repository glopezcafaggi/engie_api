import pandas as pd
import plotly.express as px
from datetime import datetime

def power_plot(data):
    fig = px.area(data, y="P_avg_predictions")
    return fig

def dist_plot(data):
    fig = px.density_heatmap(data, x="wind_speed", y="P_avg", marginal_x="histogram", marginal_y="histogram")
    return fig

def hist_plot(data):   
    fig = px.histogram(data, x="P_avg")
    return fig

def polar_wind(data): 
    fig = px.scatter_polar(data, r="P_avg", theta="wind_deg")
    return fig

def plot1(data1):
    data1['datetime'] = pd.to_datetime(data1.index, unit='s').day_of_year
    fig = px.line_polar(data1, r="P_avg", theta='datetime')
    return fig
