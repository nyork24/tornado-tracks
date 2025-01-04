import pandas as pd
from flask import Flask

# Load CSV
data = pd.read_csv('2022_torn.csv')

# Example: Parse and clean
data['start_coords'] = list(zip(data['slat'], data['slon']))
data['end_coords'] = list(zip(data['elat'], data['elon']))
data['date'] = pd.to_datetime(data['date'])
data['time'] = pd.to_datetime(data['time'])

app = Flask(__name__)

