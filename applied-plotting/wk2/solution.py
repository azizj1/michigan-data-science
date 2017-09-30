# Python 3.6.2
import matplotlib.pyplot as plt
import mplleaflet
import pandas as pd
import matplotlib.dates as mdates
from matplotlib.ticker import FuncFormatter
from matplotlib import colors

fileHash = '9f4fb72513673045265389f0be9205e3a64666064cb459a03f4a6b2b'
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

# leaflet_plot_stations(400, fileHash)

def getMaxMinTemperaturesFromCsv(filename: str):
    temperatures = pd.read_csv(filename)
    # will convert all 2005-2014 to 1900.
    temperatures = temperatures \
        .where(~temperatures['Date'].str.endswith('02-29')) \
        .dropna() \
        .replace({'Date': {r'(?!2015)^.+?-(.+)': r'1900-\1'}}, regex=True) \
        .groupby(['Element', 'Date']) \
        .agg({'Data_Value': ['min', 'max']})
    # originalTemp is a table with multiindex (Element, Date) and multi level columns
    # (Data_Value, min) (Data_Value, max)
    temperatures.index = temperatures.index.map(lambda t: (t[0], pd.to_datetime(t[1])))
    maxTemperatures = temperatures.loc['TMAX', ('Data_Value', 'max')]
    minTemperatures = temperatures.loc['TMIN', ('Data_Value', 'min')]
    return (minTemperatures, maxTemperatures)

def separate2015Temperatures(temperatures):
    # temperatures['2015'] is a series, so you can't add columns to it. Doing temperatures['1900'] will grab all data
    # that has an index in 1900, so 1900-01-01, 1900-04-18, etc.
    return pd.DataFrame({'2005-2014': temperatures['1900'], '2015': temperatures['2015'].values})

def findRecordsBrokenIn2015(temperatures, findMin=False, findMax=False):
    if findMin:
        temperatures['broken_2015'] = temperatures \
            .where(temperatures['2015'] < temperatures['2005-2014']) \
            .loc[:, '2015']
    elif findMax:
        temperatures['broken_2015'] = temperatures \
            .where(temperatures['2015'] > temperatures['2005-2014']) \
            .loc[:, '2015']
    return temperatures

def stylePlot():
    ax = plt.gca()

    # format x scale to Jan/Feb/etc.
    pltFormat = mdates.DateFormatter('%b')
    ax.xaxis.set_major_formatter(pltFormat)

    # not make the x-axis and left y-axis so harsh
    plt.xticks(alpha=0.8)
    plt.yticks(alpha=0.8)

    # some pretty formatting of the y-axis ticks
    ax.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0f} $\degree$C'.format(float(y) / 10)))

    # right y-axis, making it identical to the first barring the values
    rightAx = ax.twinx()
    rightAx.set_ylim(ax.get_ylim())
    rightAx.yaxis.set_major_formatter(FuncFormatter(lambda y, _: '{:.0f} $\degree$F'.format(float(y) / 10 * 1.8 + 32)))
    rightAx.yaxis.set_alpha(0.8)
    rightAx.tick_params(axis='y', colors=colors.to_rgba('#000000', 0.8))

    # general customization of the plot: title and add some alpha to the figure borders
    plt.title('Milwaukee, WI Temperatures\nin 2005-2014 vs. 2015', alpha=0.8)
    for spine in ax.spines.values():
        spine.set_color(colors.to_rgba('#ffffff', 0.8))


def plotGraphsWithLegend(maxTemperatures):
    plt.plot(maxTemperatures.index.values, maxTemperatures['2005-2014'], 'gray', label='2005-2014')
    plt.scatter(
        maxTemperatures.dropna().index, maxTemperatures.dropna().loc[:, 'broken_2015'], color='b', s=15, label='2015')
    plt.legend(loc=2)

def plotGraphsWithoutLegend(minTemperatures):
    plt.plot(minTemperatures.index.values, minTemperatures['2005-2014'], 'gray')
    plt.scatter(minTemperatures.dropna().index, minTemperatures.dropna().loc[:, 'broken_2015'], color='b', s=15)

def plot(minTemperatures, maxTemperatures):
    plotGraphsWithLegend(maxTemperatures) # needs to be first
    plotGraphsWithoutLegend(minTemperatures)

    plt.gca().fill_between(
        maxTemperatures.index.values,
        minTemperatures['2005-2014'],
        maxTemperatures['2005-2014'],
        facecolor='gray', alpha=0.3)

def execute():
    filename = fileDirectory + fileHash + '.csv'
    minTemperatures, maxTemperatures = getMaxMinTemperaturesFromCsv(filename)

    maxTemperatures = findRecordsBrokenIn2015(separate2015Temperatures(maxTemperatures), findMax=True)
    minTemperatures = findRecordsBrokenIn2015(separate2015Temperatures(minTemperatures), findMin=True)

    plot(minTemperatures, maxTemperatures)
    stylePlot()
    plt.show()

execute()
