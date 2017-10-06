from functools import reduce
import os
import pandas as pd
import numpy as np

MIN_STUDENTS = 0

def getFiles():
    dataDir = './data/public-schools/'
    x = [dataDir + f.name for f in os.scandir(dataDir) if f.is_file()]
    return [x[0]]

def sumStudentCount(group):
    highSchoolPopulation = group.loc[group['GROUP_BY'] == 'Grade Level', 'STUDENT_COUNT'].sum()
    year = group.loc[group.index[0], 'SCHOOL_YEAR']
    return pd.Series({
        'County': group.loc[group.index[0], 'COUNTY'],
        'DistrictName': group.loc[group.index[0], 'DISTRICT_NAME'],
        'SchoolName': group.loc[group.index[0], 'SCHOOL_NAME'],
        year: highSchoolPopulation if highSchoolPopulation > MIN_STUDENTS else np.nan
    })

def csvToDataFrame(filePath):
    data = pd.read_csv(filePath, dtype={'SCHOOL_CODE': np.str, 'DISTRICT_CODE': np.str}).dropna(subset=['SCHOOL_CODE'])
    year = data.loc[data.index[0], 'SCHOOL_YEAR']
    data = data \
        .where(data['GROUP_BY_VALUE'].str.match(r'9|10|11|12', case=True, na=False)) \
        .dropna(subset=['SCHOOL_CODE']) \
        .astype({'STUDENT_COUNT': np.int32}) \
        .groupby(['DISTRICT_CODE', 'SCHOOL_CODE', 'GROUP_BY']) \
        .agg({'STUDENT_COUNT': 'sum', 'DISTRICT_NAME': 'first', 'SCHOOL_NAME': 'first', 'COUNTY': 'first'}) \
        .reset_index() \
        .drop('GROUP_BY', axis=1) \
        .rename(columns={
            'DISTRICT_CODE': 'DistrictCode',
            'DISTRICT_NAME': 'DistrictName',
            'SCHOOL_CODE': 'SchoolCode',
            'SCHOOL_NAME': 'SchoolName',
            'COUNTY': 'County',
            'STUDENT_COUNT': year
        }) \
        .dropna()
    print(len(data.where(data[year] == 0).dropna()))
    print('Loaded {} data for {}'.format(data.shape, filePath))
    return data

def reduceData(cum, current):
    if cum is None:
        return current
    return pd.merge(cum, current, how='outer', left_index=True, right_index=True,
                    on=['County', 'DistrictName', 'SchoolName'])

def getSchools():
    return reduce(reduceData, map(csvToDataFrame, getFiles()), None)
