import publicSchools as pub
import religiousSchools as rel
import pandas as pd
from scipy import stats
from schoolsPlot import plot

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 150)

def religiousSchoolsData(startingYr: int, minStudentsEveryYr: int):
    return rel.schools(startingYr, minStudentsEveryYr).drop(['DistrictName', 'SchoolName'], axis=1)

def publicSchoolsData(startingYr: int, minStudentsEveryYr: int):
    public = pub.schools(startingYr, minStudentsEveryYr)
    return public.reset_index().drop(['DistrictCode', 'SchoolCode', 'DistrictName', 'SchoolName'], axis=1)

def getYrSignificantDifs(startingYr: int, pubData, relData):
    alpha = 0.05
    sigDiffs = []
    for i in range(startingYr, 2017):
        _, pval = stats.ttest_ind(pubData[str(i)], relData[str(i)])
        if pval < alpha:
            sigDiffs.append(i)
    return sigDiffs

def execute(minStudentsEveryYr, yrToStart):
    relSchools = religiousSchoolsData(yrToStart, minStudentsEveryYr)
    pubSchools = publicSchoolsData(yrToStart, minStudentsEveryYr)
    diffs = getYrSignificantDifs(yrToStart, pubSchools, relSchools)
    plot(pubSchools, relSchools, diffs)

execute(1, 2007)
