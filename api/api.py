from flask import Flask, render_template, url_for, redirect
import pandas as pd

import markdown
from pathlib import Path
from datetime import datetime

from pymongo import MongoClient
from bson import ObjectId

from utils.api_utils import read_all_json, read_one_json
from ml.ml_utils.pipeline import predictions
from keras.models import load_model

from utils.graph_utils import power_plot, dist_plot, hist_plot, polar_wind, plot1
import plotly.express as px
import plotly.io as pio

client = MongoClient("mongodb://localhost:27017/")

db = client["engie"]
weather_collection = db["wheater_records"]

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
def home():
    md_path = Path("Readme.md")
    md_text = md_path.read_text(encoding="utf-8")

    html = markdown.markdown(
        md_text,
        extensions=["fenced_code", "tables", "toc"]
    )

    return render_template('index.html', content=html)

@app.route('/getall')
def getall():
    #records_keys = read_all_json().keys()
    
    documents = weather_collection.find()
    records_keys = [
        [
            str(doc["_id"]),
            datetime.fromtimestamp(int(doc["raw"]["index"][0])),
            datetime.fromtimestamp(int(doc["raw"]["index"][-1]))
        ]
        for doc in documents
    ]

    return render_template('getall.html', records_keys=records_keys)

@app.route('/get/<string:id>')
def getbyid(id):
    oid = ObjectId(id)
    doc = weather_collection.find_one({"_id": oid})

    if not doc:
        return "Record not found", 404

    raw = doc['raw']
    data = pd.DataFrame(
        data = raw["data"]
        , columns = raw['columns']
        , index =  raw['index']  
    )
    data.index =  pd.to_datetime(data.index, unit='s')

    model = load_model('ml/models/model1.keras')
    data_pred = predictions(data, model)
    #print(data_pred.head(1))
    #print(data_pred.shape)

    pwr_plt = power_plot(data_pred)
    dst_plt = dist_plot(data)
    hst_plt = hist_plot(data)
    plr_wind = polar_wind(data)

    pwr_plt_html = pio.to_html(
        pwr_plt,
        full_html=False,
        include_plotlyjs="cdn"
    )

    dst_plt_html = pio.to_html(
        dst_plt,
        full_html=False,
        include_plotlyjs="cdn"
    )

    hst_plt_html = pio.to_html(
        hst_plt,
        full_html=False,
        include_plotlyjs="cdn"
    )

    plr_wind_html = pio.to_html(
        plr_wind,
        full_html=False,
        include_plotlyjs="cdn"
    )

    data_html = data.head().to_html(classes="table table-striped", index=True)
    data_pred_html = data_pred.head().to_html(classes="table table-striped", index=True)
    
    return render_template(
        'getbyid.html'
        , id=id
        , data = data_html
        , data_pred = data_pred_html
        , pwr_plt_html = pwr_plt_html
        , dst_plt_html = dst_plt_html
        , hst_plt_html = hst_plt_html
        , plr_wind_html = plr_wind_html   )


if __name__ == '__main__':
    app.run(debug=True)