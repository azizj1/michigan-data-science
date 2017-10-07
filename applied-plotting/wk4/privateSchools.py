from functools import reduce
import os
import pandas as pd

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
    x = [PrivateSchoolFile(dataDir + f.name) for f in os.scandir(dataDir) if f.is_file() & (f.name != '.DS_Store')]
    return x

def excelToDataFrame(file: PrivateSchoolFile):
    data = pd \
        .read_excel(file.path, sheetname=2, skiprows=file.skiprows) \
        .dropna(axis=1, how='all') \
        .dropna(subset=['School']) \
        .filter(regex=r'School|District|9th|10th|11th|12th|(Sch Code)')
    data.columns = ['District', 'SchoolCode', 'School', '9', '10', '11', '12']
    data.loc[:, file.year] = data['9'] + data['10'] + data['11'] + data['12']
    data = data[['District', 'SchoolCode', 'School', file.year]] \
            .where(data[file.year] > 0) \
            .dropna() \
            .set_index('SchoolCode')
    return data

def reduceData(cum, curr):
    if cum is None:
        return curr
    return pd.merge(curr, cum, how='outer', left_index=True, right_index=True, on=['District', 'School'])

def getSchools():
    return reduce(reduceData, map(excelToDataFrame, getFiles()), None)
