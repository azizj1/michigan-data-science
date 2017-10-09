import re
import pandas as pd

def reduceArrayOfDfs(cum, curr):
    if cum is None:
        return curr
    return pd.merge(curr, cum, how='outer', left_index=True, right_index=True,
                    on=['DistrictName', 'SchoolName']).fillna(0)

def filterColumnsToStartingYr(df, startingYr):
    if startingYr <= 2007:
        return df
    dfCopy = df.copy()
    dfCopy.columns = dfCopy.columns.map(str)
    # minus 1 because we need the year before it to calculate its growth rate
    return dfCopy.drop([str(x) for x in range(2006, startingYr - 1)], axis=1)

# helper function for addYTYChangeToDf
def groupColumnForDif(colName):
    colName = str(colName)
    group = str(int(colName[:-2]) + 1) if colName[-1] == 'L' else colName
    return 'ChangeFrom{}To{}'.format(str(int(group) - 1), group)

# copy all the data, add the string '-L' to the names, so 2006-L, 2007-L, multiply those values by -1 because we'll
# be using those to subtract. Then, merge them with the orignal (so 2006, 2007, etc.), and group 2006-L and 2007 with
# 'Growth in 2007', group 2007-L and 2008 with 'Growth in 2008', etc. Finally, just sum the groups and you're done
def addYTYChangeToDf(df):
    dfCopy = df.drop(['DistrictName', 'SchoolName'], axis=1)
    dfCopy.columns = dfCopy.columns.map(str)
    startingYr = min([int(x) for x in dfCopy.columns if re.match(r'^\d+$', x)])

    dfCopy = pd \
        .merge(dfCopy.rename(columns=lambda name: str(name) + '-L') * -1, dfCopy, left_index=True, right_index=True) \
        .drop([str(startingYr), '2016-L'], axis=1) \
        .groupby(groupColumnForDif, axis=1) \
        .sum()
    return pd.merge(df, dfCopy, right_index=True, left_index=True)

def addGrowthRate(df):
    dfCopy = df.copy()
    dfCopy.columns = dfCopy.columns.map(str)
    startingYr = min([int(x) for x in dfCopy.columns if re.match(r'^\d+$', x)])

    numOfStudents = dfCopy.loc[:, [str(i) for i in range(startingYr, 2016)]]
    changeInStudents = dfCopy.loc[:, ['ChangeFrom{}To{}'.format(str(i), str(i+1)) for i in range(startingYr, 2016)]]
    growthValues = changeInStudents.values / numOfStudents.values
    growthDf = pd.DataFrame(growthValues,
                            columns=['GrowthIn' + str(i+1) for i in range(startingYr, 2016)],
                            index=dfCopy.index)
    return pd.merge(df, growthDf, left_index=True, right_index=True)

def filterRows(df, minStudentsEveryYr):
    return df.where(df >= minStudentsEveryYr).dropna()

# remove the 2006, 2007, ..., ChangeFrom2006To2007,.. columns, and then rename GrowthInXXXX to XXXX
def filterColumnsToGrowth(df):
    return df.filter(regex=r'^(?!20\d\d)(?!ChangeFrom.*)') \
             .rename(columns=lambda name: re.sub(r'GrowthIn(\d+)', r'\1', name))

def religiousSchoolsNameChanges():
    return {
        r'\bSt\.': r'Saint',
        r'\bSt\b': r'Saint',
        r'\s?Middle/High School\s?': r'',
        r'\s?El/Sec\s?': r'',
        r'\s?Elementary/Secondary\s?': r'',
        r'Dr\.': r'Dr',
        r'Eagle Christian': r'Eagle',
        r'the Sacred Heart': r'Sacred Heart',
        r'\s?High\s?': r'',
        r'\s?Hi\s?': r'',
        r'\s?School\s?': r'',
        r'\s?Schs?\b': r'',
        r'\s?College\s?': r'',
        r'Pt': r'Point',
        r'Acad(?!e)': r'Academy',
        r'\s?of Milwaukee': r'',
        r'\s?of Milw': r'',
        r'\'': r'',
        r'Christ Christian': r'Christ',
        r'Bay City Baptist': r'Bay City Christian',
        r'Berean Christian': r'Berean Baptist Christian',
        r'WI': r'Wisconsin',
        r'Lourdes Academy': r'Lourdes',
        r'Pius XI Catholic': r'Pius XI',
        r'Roncalli Catholic': r'Roncalli',
        r'\s?Inc\s?': r''
    }
