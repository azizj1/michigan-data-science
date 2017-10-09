from functools import reduce
import os
import pandas as pd
from common import \
    reduceArrayOfDfs, \
    addYTYChangeToDf, \
    addGrowthRate, \
    filterRows, \
    filterColumnsToGrowth, \
    filterColumnsToStartingYr

class PrivateSchoolFile:
    def __init__(self, path):
        self.path = path
        self.year = (int(path[-7:-5]) if path[-1] == 'x' else int(path[-6:-4])) - 1
        self.year += 2000
        if self.year <= 2009:
            self.skiprows = 0
        elif self.year == 2014: # for school year 2014-15, skip 2 rows
            self.skiprows = 2
        else:
            self.skiprows = 1

def getFiles():
    dataDir = './data/private-schools/'
    return [PrivateSchoolFile(dataDir + f.name) for f in os.scandir(dataDir) if f.is_file() & (f.name != '.DS_Store')]

def excelToDataFrame(file: PrivateSchoolFile):
    data = pd \
        .read_excel(file.path, sheetname=2, skiprows=file.skiprows) \
        .dropna(axis=1, how='all') \
        .dropna(subset=['School']) \
        .filter(regex=r'School|District|9th|10th|11th|12th|(Sch Code)')
    data.columns = ['DistrictName', 'SchoolCode', 'SchoolName', '9', '10', '11', '12']
    data.loc[:, file.year] = data['9'] + data['10'] + data['11'] + data['12']

    return data[['DistrictName', 'SchoolCode', 'SchoolName', file.year]] \
            .where(data[file.year] > 0) \
            .dropna() \
            .set_index('SchoolCode')

def schools(startingYr: int = 2007, minStudentsEveryYr: int = 0):
    df = filterColumnsToStartingYr(reduce(reduceArrayOfDfs, map(excelToDataFrame, getFiles()), None), startingYr)
    return filterColumnsToGrowth(addGrowthRate(addYTYChangeToDf(filterRows(df, minStudentsEveryYr))))
