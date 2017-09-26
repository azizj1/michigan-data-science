import re
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 150)

states = {'OH': 'Ohio', 'KY': 'Kentucky', 'AS': 'American Samoa', 'NV': 'Nevada', 'WY': 'Wyoming', 'NA': 'National',
          'AL': 'Alabama', 'MD': 'Maryland', 'AK': 'Alaska', 'UT': 'Utah', 'OR': 'Oregon', 'MT': 'Montana',
          'IL': 'Illinois', 'TN': 'Tennessee', 'DC': 'District of Columbia', 'VT': 'Vermont', 'ID': 'Idaho',
          'AR': 'Arkansas', 'ME': 'Maine', 'WA': 'Washington', 'HI': 'Hawaii', 'WI': 'Wisconsin', 'MI': 'Michigan',
          'IN': 'Indiana', 'NJ': 'New Jersey', 'AZ': 'Arizona', 'GU': 'Guam', 'MS': 'Mississippi', 'PR': 'Puerto Rico',
          'NC': 'North Carolina', 'TX': 'Texas', 'SD': 'South Dakota', 'MP': 'Northern Mariana Islands', 'IA': 'Iowa',
          'MO': 'Missouri', 'CT': 'Connecticut', 'WV': 'West Virginia', 'SC': 'South Carolina', 'LA': 'Louisiana',
          'KS': 'Kansas', 'NY': 'New York', 'NE': 'Nebraska', 'OK': 'Oklahoma', 'FL': 'Florida', 'CA': 'California',
          'CO': 'Colorado', 'PA': 'Pennsylvania', 'DE': 'Delaware', 'NM': 'New Mexico', 'RI': 'Rhode Island',
          'MN': 'Minnesota', 'VI': 'Virgin Islands', 'NH': 'New Hampshire', 'MA': 'Massachusetts', 'GA': 'Georgia',
          'ND': 'North Dakota', 'VA': 'Virginia'}

def isState(line: str):
    return line.endswith('[edit]')

def cleanState(line: str):
    return line.replace('[edit]', '')

def cleanCity(line: str):
    return re.sub(r' \(.+$', '', line)

def get_list_of_university_towns():
    stateTownsList = []

    with open("university_towns.txt", encoding="utf-8") as file:
        currentState = None

        for line in file:
            line = line.strip()
            if isState(line):
                currentState = cleanState(line)
            else:
                stateTownsList.append((currentState, cleanCity(line)))

    return pd.DataFrame(stateTownsList, columns=["State", "RegionName"])

def yearMoToYearQuarter(yearMo: str):
    yearMo = yearMo.split('-')
    month = int(yearMo[1])
    quarter = int((month - 1) / 3) + 1
    return yearMo[0] + 'q' + str(quarter)

def convert_housing_data_to_quarters():
    return pd.read_csv('City_Zhvi_AllHomes.csv') \
            .replace({'State': states}) \
            .set_index(['State', 'RegionName']) \
            .iloc[:, 49:] \
            .groupby(yearMoToYearQuarter, axis=1) \
            .mean()

def readGdp():
    gdp = pd.read_excel('gdplev.xls', sheetname=0, skiprows=8, header=None).iloc[:, [4,6]]
    gdp.columns = ['year-quarter', 'gdp']
    startIndex = gdp.loc[(gdp['year-quarter'] == '2000q1'), :].index[0]
    gdp = gdp.iloc[startIndex:, :]
    gdp['diff'] = gdp['gdp'] - gdp['gdp'].shift(1)
    return gdp.set_index('year-quarter')

def get_recession_start():
    gdp = readGdp()
    return gdp[(gdp['diff'] < 0) & (gdp['diff'].shift(-1) < 0)].index[0]

def get_recession_end():
    gdp = readGdp()
    recessionStart = get_recession_start()
    return gdp.loc[recessionStart:, :].where((gdp['diff'] > 0) & (gdp['diff'].shift(1) > 0)).dropna().index[0]

def get_recession_bottom():
    gdp = readGdp()
    recessionStart = get_recession_start()
    recessionEnd = get_recession_end()
    return gdp.loc[recessionStart:recessionEnd, 'gdp'].idxmin()

print(get_recession_start())
print(get_recession_end())
print(get_recession_bottom())
