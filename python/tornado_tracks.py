from flask import Flask, jsonify, render_template, send_from_directory
from flask_cors import CORS
import pandas as pd
from earthengine.mosiac import *

app = Flask(__name__)
CORS(app)

data = pd.read_csv('python/2022_torn.csv', index_col='om', usecols=['om', 'yr', 'mo', 'dy', 'time', 'st', 'mag', 'loss', 'slat', 'slon', 'elat', 'elon', 'len', 'wid'])
data['start_coords'] = list(zip(data['slat'], data['slon']))
data['end_coords'] = list(zip(data['elat'], data['elon']))

@app.route("/")
def index():
    return send_from_directory("./", "index.html")

@app.route("/api/get_options")
def get_options():
    options = [
        {
            'value': idx,  # Use date as unique value
            'label': f"{row['yr']}/{row['mo']:02d}/{row['dy']:02d}, Magnitude: {row['mag']}"
        }
        for idx, row in data.iterrows()
    ]
    return options

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

    return jsonify({"url": img_link_before,
                    "lat1": lat1,
                    "lon1": lon1,
                    "lat2": lat2,
                    "lon2": lon2})

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

    return jsonify({"url": img_link_after,
                    "lat1": lat1,
                    "lon1": lon1,
                    "lat2": lat2,
                    "lon2": lon2})

def main():
    print(data.to_dict(orient='records'))

if (__name__ == "__main__"):
    main();