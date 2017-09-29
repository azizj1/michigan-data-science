import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from matplotlib import colors

fileName = '9f4fb72513673045265389f0be9205e3a64666064cb459a03f4a6b2b'
fileDirectory = '' #'data/C2A2_data/BinnedCsvs_d400/'
binDirectory = '' #'data/C2A2_data/'

def leaflet_plot_stations(binsize, hashid):

    df = pd.read_csv('{}BinSize_d{}.csv'.format(binDirectory, binsize))

    station_locations_by_hash = df[df['hash'] == hashid]
    print(station_locations_by_hash)
    lons = station_locations_by_hash['LONGITUDE'].tolist()
    lats = station_locations_by_hash['LATITUDE'].tolist()

    plt.figure(figsize=(8, 8))

    plt.scatter(lons, lats, c='r', alpha=0.7, s=200)

    return mplleaflet.show()

# leaflet_plot_stations(400, fileName)

def highLowsPlots():
    originalTemp = pd.read_csv(fileDirectory + fileName + '.csv')
    # will convert all 2005-2014 to 1900.
    originalTemp = originalTemp \
        .where(~originalTemp['Date'].str.endswith('02-29')) \
        .dropna() \
        .replace({'Date': {r'(?!2015)^.+?-(.+)': r'1900-\1'}}, regex=True) \
        .groupby(['Element', 'Date']) \
        .agg({'Data_Value': ['min', 'max']})
    # originalTemp is a table with multiindex (Element, Date) and multi level columns
    # (Data_Value, min) (Data_Value, max)
    originalTemp.index = originalTemp.index.map(lambda t: (t[0], pd.to_datetime(t[1])))
    maxAllData = originalTemp.loc['TMAX', ('Data_Value', 'max')]
    minAllData = originalTemp.loc['TMIN', ('Data_Value', 'min')]

    # maxAllData['2015'] is a series, so you can't add columns to it. Doing maxAllData['1900'] will grab all data
    # that has an index in 1900, so 1900-01-01, 1900-04-18, etc.
    maxAllData = pd.DataFrame({'2005-2014': maxAllData['1900'], '2015': maxAllData['2015'].values})
    minAllData = pd.DataFrame({'2005-2014': minAllData['1900'], '2015': minAllData['2015'].values})

    maxAllData['broken_2015'] = maxAllData.where(maxAllData['2015'] > maxAllData['2005-2014']).loc[:, '2015']
    minAllData['broken_2015'] = minAllData.where(minAllData['2015'] < minAllData['2005-2014']).loc[:, '2015']
    maxAllData_dates = maxAllData.index.values

    ax = plt.gca()
    plt.plot(maxAllData_dates, maxAllData['2005-2014'], 'gray', label='2005-2014')
    plt.scatter(maxAllData.dropna().index, maxAllData.dropna().loc[:, 'broken_2015'], color='b', s=15, label='2015')
    plt.legend(loc=2)

    plt.plot(maxAllData_dates, minAllData['2005-2014'], 'gray')
    plt.scatter(minAllData.dropna().index, minAllData.dropna().loc[:, 'broken_2015'], color='b', s=15)
    ax.fill_between(maxAllData_dates, maxAllData['2005-2014'],
                    minAllData['2005-2014'], facecolor='gray', alpha=0.3)

    pltFormat = mdates.DateFormatter('%b')
    plt.xticks(alpha=0.8)
    plt.yticks(alpha=0.8)
    ax.xaxis.set_major_formatter(pltFormat)
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0f} $\degree$C'.format(float(y) / 10)))
    rightAx = ax.twinx()
    rightAx.set_ylim(ax.get_ylim())
    rightAx.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0f} $\degree$F'.format(float(y) / 10 * 1.8 + 32)))
    rightAx.yaxis.set_alpha(0.8)
    rightAx.tick_params(axis='y', colors=colors.to_rgba('#000000', 0.8))
    plt.title('Milwaukee, WI Temperatures\nin 2005-2014 vs. 2015', alpha=0.8)
    for spine in plt.gca().spines.values():
        spine.set_color(colors.to_rgba('#ffffff', 0.8))
    plt.show()


highLowsPlots()
