from flask import Flask, jsonify
import pandas as pd
from earthengine.mosiac import *

app = Flask(__name__)
data = pd.read_csv('2022_torn.csv', index_col='om', usecols=['om', 'yr', 'mo', 'dy', 'time', 'st', 'mag', 'loss', 'slat', 'slon', 'elat', 'elon', 'len', 'wid'])
data['start_coords'] = list(zip(data['slat'], data['slon']))
data['end_coords'] = list(zip(data['elat'], data['elon']))

@app.route("/")
def index():
    return "<p>Tornado Tracks</p>"

@app.route("/satellite/before/<int:id>")
def image():
    tornado_data = data[data.om.isin([id])]
    dy = tornado_data.iloc[0]['dy']
    mo = tornado_data.iloc[0]['mo']
    yr = tornado_data.iloc[0]['yr']
    lat1 = tornado_data.iloc[0]['slat']
    lon1 = tornado_data.iloc[0]['slon']
    lat2 = tornado_data.iloc[0]['elat']
    lon2 = tornado_data.iloc[0]['elon']

    img_link_before = get_before_image(dy, mo, yr, lat1, lon1, lat2, lon2)

    return '<img src=' + img_link_before + '>'

@app.route("/satellite/after/<int:id>")
def image():
    tornado_data = data[data.om.isin([id])]
    dy = tornado_data.iloc[0]['dy']
    mo = tornado_data.iloc[0]['mo']
    yr = tornado_data.iloc[0]['yr']
    lat1 = tornado_data.iloc[0]['slat']
    lon1 = tornado_data.iloc[0]['slon']
    lat2 = tornado_data.iloc[0]['elat']
    lon2 = tornado_data.iloc[0]['elon']

    img_link_after = get_after_image(dy, mo, yr, lat1, lon1, lat2, lon2)

    return '<img src=' + img_link_after + '>'
