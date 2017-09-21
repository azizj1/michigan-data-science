import pandas as pd
import numpy as np

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 200)

def getEnergy():
    # Energy Indicators.xls cleaning
    energy = pd.read_excel('Energy Indicators.xls', sheetname=0, skip_footer=38, skiprows=18, header=None)
    energy = energy[[2, 3, 4, 5]]
    energy.columns = ['Country', 'Energy Supply', 'Energy Supply per Capita', '% Renewable']
    energy.loc[energy['Energy Supply'] == '...', 'Energy Supply'] = np.NaN
    energy.loc[energy['Energy Supply per Capita'] == '...', 'Energy Supply per Capita'] = np.NaN
    energy.loc[:, 'Energy Supply'] *= 1000000

    energyRenames = {
        'Republic of Korea': 'South Korea',
        'United States of America': 'United States',
        'United Kingdom of Great Britain and Northern Ireland': 'United Kingdom',
        'China, Hong Kong Special Administrative Region': 'Hong Kong'
    }
    energy.loc[:, 'Country'].replace(regex=True, inplace=True, to_replace={r'(\s?\(.*?\)|\d+)' : r''})
    energy.replace(to_replace=energyRenames, inplace=True)
    return energy

def getGdp():
    # world_bank.csv cleaning
    GDP = pd.read_csv('world_bank.csv', skiprows=4)
    gdpRenames = {
        'Korea, Rep.': 'South Korea',
        'Iran, Islamic Rep.': 'Iran',
        'Hong Kong SAR, China': 'Hong Kong'
    }
    GDP.replace(to_replace=gdpRenames, inplace=True)
    gdpColumnsToKeep = ['Country Name', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    GDP = GDP[gdpColumnsToKeep]
    return GDP

def getScimEn():
    return pd.read_excel('scimagojr-3.xlsx')

def merge(energy, GDP, ScimEn):
    mergeDf = pd.merge(energy, GDP, how='inner', left_on='Country', right_on='Country Name')
    mergeDf = pd.merge(mergeDf, ScimEn, how='inner', on='Country')
    return mergeDf

def answer():
    energy = getEnergy()
    GDP = getGdp()
    ScimEn = getScimEn()

    # merge
    mergeDf = merge(energy, GDP, ScimEn)
    mergeColumnsToKeep = ['Country', 'Rank', 'Documents', 'Citable documents', 'Citations', 'Self-citations',
                          'Citations per document', 'H index', 'Energy Supply', 'Energy Supply per Capita',
                          '% Renewable', '2006', '2007', '2008', '2009', '2010', '2011', '2012', '2013', '2014', '2015']
    mergeDf = mergeDf[mergeColumnsToKeep].sort_values('Rank').head(15).set_index('Country')
    return mergeDf

__version__ = '1.0'
