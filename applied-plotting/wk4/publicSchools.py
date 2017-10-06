from functools import reduce
import os
import pandas as pd
import numpy as np

MIN_STUDENTS = 0

def getFiles():
    dataDir = './data/public-schools/'
    return [dataDir + f.name for f in os.scandir(dataDir) if f.is_file()]

def sumStudentCount(group):
    highSchoolPopulation = group \
        .loc[group['GROUP_BY'] == 'Grade Level', 'STUDENT_COUNT'] \
        .astype(int) \
        .sum()
    # append(0) below in case the .loc returns an empty set (no-male school), so that when we do .values[0],
    # it doesn't crash
    malePercent = group \
        .loc[group['GROUP_BY_VALUE'] == 'Male', 'PERCENT_OF_GROUP'] \
        .append([pd.Series([0])]) \
        .astype(float) \
        .values[0]
    totalMales = int(np.rint(malePercent * 0.01 * highSchoolPopulation))
    year = group.loc[group.index[0], 'SCHOOL_YEAR']
    return pd.Series({
        year: highSchoolPopulation if highSchoolPopulation > MIN_STUDENTS else np.nan,
        'County': group.loc[group.index[0], 'COUNTY'],
        'DistrictName': group.loc[group.index[0], 'DISTRICT_NAME'],
        'SchoolName': group.loc[group.index[0], 'SCHOOL_NAME'],
        year + '-Male': totalMales,
        year + '-Female': highSchoolPopulation - totalMales
    })

def csvToDataFrame(filePath):
    data = pd.read_csv(filePath, dtype={'SCHOOL_CODE': np.str, 'DISTRICT_CODE': np.str}).dropna(subset=['SCHOOL_CODE'])
    data = data \
        .where( \
            (data['GROUP_BY_VALUE'].str.match(r'9|10|11|12|Male|Female', case=True, na=False)) & \
            (~data['GRADE_GROUP'].str.match('Elementary School'))) \
        .dropna(subset=['SCHOOL_CODE']) \
        .groupby(['DISTRICT_CODE', 'SCHOOL_CODE']) \
        .apply(sumStudentCount) \
        .dropna()
    print('Loaded {} data for {}'.format(data.shape, filePath))
    return data

def reduceData(cum, current):
    if cum is None:
        return current
    return pd.merge(cum, current, how='outer', left_index=True, right_index=True)

def getSchools():
    return reduce(reduceData, map(csvToDataFrame, getFiles()), None)
