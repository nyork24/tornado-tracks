import pandas as pd
import numpy as np

from earthengine.mosiac import *

# Load CSV
# moving csv into python dir for testing rememer to put back in /data
data = pd.read_csv('python/2022_torn.csv', index_col='om', usecols=['om', 'date', 'time', 'st', 'mag', 'loss', 'slat', 'slon', 'elat', 'elon', 'len', 'wid'])

# Example: Parse and clean
data['start_coords'] = list(zip(data['slat'], data['slon']))
data['end_coords'] = list(zip(data['elat'], data['elon']))
#data.drop(['slat', 'slon', 'elat', 'elon'], axis=1, inplace=True)

"""
Parses a date in format YYYY-MM-DD, and returns integers in form year, month, day
"""
def parse_date(date):
    lst = date.split('-')
    year = int(lst[0])
    month = int(lst[1])
    day = int(lst[2])
    return year, month, day

"""
data[column label] - returns a series equivelent to the data within the column in each entry
data.loc[row value] - returns a series equivelent to the data in each entry matching the row label
"""

def main():
    print(data)
    print(data['len'])
    print(data.loc[620940])
    # create dataframe with only the ef3 tornados from greater dataframe
    only_ef4 = data[data.mag.isin([4])]
    only_ef3 = data[data.mag.isin([3])]
    print(only_ef4)
    print(only_ef3)

    for index, row in only_ef4.iterrows():
        print("Index: " + str(index));
        year, month, day = parse_date(row['date'])

        slat = row['slat']
        slon = row['slon']
        elat = row['elat']
        elon = row['elon']

        print(get_before_image(year, month, day, slat, slon, elat, elon))
        print(get_after_image(year, month, day, slat, slon, elat, elon))


main()