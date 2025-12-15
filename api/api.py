from flask import Flask, render_template, url_for, redirect
import pandas as pd

from utils.api_utils import read_all_json, read_one_json

app = Flask(__name__)

@app.route('/')
def index():
    return redirect('/home')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/getall')
def getall():
    records_keys = read_all_json().keys()
    #print(records_keys)
    #records = ['data1', 'data2']
    return render_template('getall.html', records_keys=records_keys)

@app.route('/get/<id>')
def getbyid(id):
    data = read_one_json(id)
    #data_pred = power_prediction(data)

    data_html = data.head().to_html(classes="table table-striped", index=True) 
    #data_pred_html = data_pred.to_html(classes="table table-striped", index=True) 
    return render_template('getbyid.html', id=id, data_html=data_html)

if __name__ == '__main__':
    app.run(debug=True)