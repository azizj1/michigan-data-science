from functools import reduce
import os
import pandas as pd
import numpy as np
from common import \
    reduceArrayOfDfs, \
    addYTYChangeToDf, \
    addGrowthRate, \
    filterRows, \
    filterColumnsToGrowth, \
    filterColumnsToStartingYr

def getFiles():
    dataDir = './data/public-schools/'
    return [dataDir + f.name for f in os.scandir(dataDir) if f.is_file() & (f.name != '.DS_Store')]

def csvToDataFrame(filePath):
    data = pd.read_csv(filePath, dtype={'SCHOOL_CODE': np.str, 'DISTRICT_CODE': np.str}).dropna(subset=['SCHOOL_CODE'])
    year = data.loc[data.index[0], 'SCHOOL_YEAR'][:-3]

    return data \
        .where( \
            (data['GROUP_BY_VALUE'].str.match(r'9|10|11|12', case=True, na=False)) & \
            (~data['GRADE_GROUP'].str.match('Elementary School'))) \
        .dropna(subset=['SCHOOL_CODE']) \
        .astype({'STUDENT_COUNT': np.int32}) \
        .groupby(['DISTRICT_CODE', 'SCHOOL_CODE', 'GROUP_BY']) \
        .agg({'STUDENT_COUNT': 'sum', 'DISTRICT_NAME': 'first', 'SCHOOL_NAME': 'first'}) \
        .reset_index() \
        .drop('GROUP_BY', axis=1) \
        .rename(columns={
            'DISTRICT_CODE': 'DistrictCode',
            'DISTRICT_NAME': 'DistrictName',
            'SCHOOL_CODE': 'SchoolCode',
            'SCHOOL_NAME': 'SchoolName',
            'STUDENT_COUNT': year
        }) \
        .set_index(['DistrictCode', 'SchoolCode']) \
        .dropna()

def schools(startingYr: int = 2007, minStudentsEveryYr: int = 0):
    df = filterColumnsToStartingYr(reduce(reduceArrayOfDfs, map(csvToDataFrame, getFiles()), None), startingYr)
    return filterColumnsToGrowth(addGrowthRate(addYTYChangeToDf(filterRows(df, minStudentsEveryYr))))
