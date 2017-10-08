from functools import reduce
import os
import pandas as pd
import numpy as np

def getFiles():
    dataDir = './data/public-schools/'
    return [dataDir + f.name for f in os.scandir(dataDir) if f.is_file()]

def csvToDataFrame(filePath):
    data = pd.read_csv(filePath, dtype={'SCHOOL_CODE': np.str, 'DISTRICT_CODE': np.str}).dropna(subset=['SCHOOL_CODE'])
    year = data.loc[data.index[0], 'SCHOOL_YEAR']

    data = data \
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
            'STUDENT_COUNT': year[:-3]
        }) \
        .set_index(['DistrictCode', 'SchoolCode']) \
        .dropna()
    print('Loaded {} data for {}'.format(data.shape, filePath))
    return data

def reduceData(cum, curr):
    if cum is None:
        return curr
    return pd.merge(cum, curr, how='outer', left_index=True, right_index=True,
                    on=['DistrictName', 'SchoolName']).fillna(0)

def groupColumnForDif(colName):
    colName = str(colName)
    group = str(int(colName[:-2]) + 1) if colName[-1] == 'L' else colName
    return 'Growth in ' + group

def addGrowthToDataFrame(df):
    dfCopy = df.drop(['DistrictName', 'SchoolName'], axis=1)
    dfCopy = pd \
        .merge(dfCopy.rename(columns=lambda name: str(name) + '-L') * -1, dfCopy, left_index=True, right_index=True) \
        .drop(['2006', '2016-L'], axis=1) \
        .groupby(groupColumnForDif, axis=1) \
        .sum()
    return pd.merge(df, dfCopy, right_index=True, left_index=True)

def getSchools():
    return addGrowthToDataFrame(reduce(reduceData, map(csvToDataFrame, getFiles()), None))
