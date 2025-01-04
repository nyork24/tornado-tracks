import pandas as pd
import numpy as np

# Load CSV
data = pd.read_csv('2022_torn.csv', index_col='om', usecols=['om', 'date', 'time', 'st', 'mag', 'loss', 'slat', 'slon', 'elat', 'elon', 'len', 'wid'])

# Example: Parse and clean
data['start_coords'] = list(zip(data['slat'], data['slon']))
data['end_coords'] = list(zip(data['elat'], data['elon']))
#data.drop(['slat', 'slon', 'elat', 'elon'], axis=1, inplace=True)


"""
data[column label] - returns a series equivelent to the data within the column in each entry
data.loc[row value] - returns a series equivelent to the data in each entry matching the row label
"""

def main():
    print(data)
    print(data['len'])
    print(data.loc[620940])
    only_ef3 = data[data.mag.isin([3])]
    print(only_ef3)



main()