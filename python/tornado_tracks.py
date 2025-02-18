from flask import Flask, jsonify, render_template, send_from_directory
import pandas as pd
from earthengine.mosiac import *

app = Flask(__name__)
data = pd.read_csv('data/2022_torn.csv', index_col='om', usecols=['om', 'yr', 'mo', 'dy', 'time', 'st', 'mag', 'loss', 'slat', 'slon', 'elat', 'elon', 'len', 'wid'])
data['start_coords'] = list(zip(data['slat'], data['slon']))
data['end_coords'] = list(zip(data['elat'], data['elon']))

@app.route("/")
def index():
    return send_from_directory("./", "index.html")

@app.route("/satellite/before/<int:id>")
def before_image(id):
    tornado_data = data.loc[id]
    dy = tornado_data[0]
    mo = tornado_data[1]
    yr = tornado_data[2]
    lat1 = tornado_data[7]
    lon1 = tornado_data[8]
    lat2 = tornado_data[9]
    lon2 = tornado_data[10]

    img_link_before = get_before_image(dy, mo, yr, lat1, lon1, lat2, lon2)

    return '<img src=' + img_link_before + '>'

@app.route("/satellite/after/<int:id>")
def after_image(id):
    tornado_data = data.loc[id]
    dy = tornado_data[0]
    mo = tornado_data[1]
    yr = tornado_data[2]
    lat1 = tornado_data[7]
    lon1 = tornado_data[8]
    lat2 = tornado_data[9]
    lon2 = tornado_data[10]

    img_link_after = get_after_image(dy, mo, yr, lat1, lon1, lat2, lon2)

    return '<img src=' + img_link_after + '>'