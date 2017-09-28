import matplotlib.pyplot as plt
import mplleaflet
import numpy as np
import pandas as pd

fileName = '9f4fb72513673045265389f0be9205e3a64666064cb459a03f4a6b2b'

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('BinSize_d{}.csv'.format(binsize))

    station_locations_by_hash = df[df['hash'] == hashid]
    print(station_locations_by_hash)
    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8, 8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.show()

# leaflet_plot_stations(400, fileName)

def highLowsPlots():
    originalTemp = pd.read_csv(fileName + '.csv')
    originalTemp = originalTemp.where(~originalTemp['Date'].str.endswith('02-29')).dropna().sort_values(by='Date')
    originalTemp.loc[:, 'Date'] = pd.to_datetime(originalTemp['Date'])
    originalTemp.set_index('Date', inplace=True)

    temp = originalTemp['2005':'2014']
    tempMax = temp[temp['Element'] == 'TMAX'].groupby(level=0).max()
    tempMin = temp[temp['Element'] == 'TMIN'].groupby(level=0).min()

    temp2015 = originalTemp['2015']
    temp2015max = pd.concat([temp2015[temp2015['Element'] == 'TMAX'].groupby(level=0).max()]*10)
    temp2015max['New_Date'] = tempMax.index
    temp2015max.set_index('New_Date', inplace=True)
    temp2015min = pd.concat([temp2015[temp2015['Element'] == 'TMIN'].groupby(level=0).min()]*10)
    temp2015min['New_Date'] = tempMin.index
    temp2015min.set_index('New_Date', inplace=True)

    tempMax['Broken_Record_2015'] = temp2015max.where(temp2015max['Data_Value'] > tempMax['Data_Value']).loc[:, 'Data_Value']
    tempMin['Broken_Record_2015'] = temp2015min.where(temp2015min['Data_Value'] < tempMin['Data_Value']).loc[:, 'Data_Value']

    plt.plot(
        tempMax.index, tempMax['Data_Value'],
        tempMin.index, tempMin['Data_Value'])

    plt.gca().fill_between(tempMin.index, tempMax['Data_Value'], tempMin['Data_Value'], facecolor='red', alpha=0.8)

    plt.scatter(tempMax.dropna().index, tempMax.dropna().loc[:, 'Broken_Record_2015'], color='g', s=10)
    plt.scatter(tempMin.dropna().index, tempMin.dropna().loc[:, 'Broken_Record_2015'], color='g', s=10)
    plt.show()

highLowsPlots()
