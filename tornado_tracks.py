from flask import Flask, jsonify
import pandas as pd
from earthengine.mosiac import *

app = Flask(__name__)
data = pd.read_csv('2022_torn.csv', index_col='om', usecols=['om', 'date', 'time', 'st', 'mag', 'loss', 'slat', 'slon', 'elat', 'elon', 'len', 'wid'])
data['start_coords'] = list(zip(data['slat'], data['slon']))
data['end_coords'] = list(zip(data['elat'], data['elon']))

@app.route("/")
def index():
    return "<p>Tornado Tracks</p>"

@app.route("/satellite/<int:id>")
def get_image():
    img_link_before = ""
    img_link_after = ""
    return '<img src=' + img_link_before + '>' + '<img src=' + img_link_after + '>'
