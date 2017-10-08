import privateSchools as priv
import publicSchools as pub
import religiousSchools as rel
from common import religiousSchoolsNameChanges
import pandas as pd
from scipy import stats

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 150)


def religiousSchoolsAvgGrowth(minStudentsEveryYr: int):
    privateSchools = priv.schools(minStudentsEveryYr).replace({'SchoolName': religiousSchoolsNameChanges()}, regex=True)
    religiousSchools = rel.schools().replace(religiousSchoolsNameChanges(), regex=True).drop_duplicates()

    return pd.merge(privateSchools, religiousSchools, how='inner', on='SchoolName') \
            .drop(['DistrictName', 'SchoolName'], axis=1)

def publicSchoolsAvgGrowth(minStudentsEveryYr: int):
    public = pub.schools(minStudentsEveryYr)
    return public.reset_index().drop(['DistrictCode', 'SchoolCode', 'DistrictName', 'SchoolName'], axis=1)

minStudents = 1

relSchools = religiousSchoolsAvgGrowth(minStudents)
print(relSchools)
# relSchools.index = relSchools.index.map(str)
# pop = relSchools.loc[[str(i) for i in range(2006, 2016)]].reset_index()
# changes = relSchools.loc[['ChangeFrom{}To{}'.format(str(i), str(i+1)) for i in range(2006, 2016)]].reset_index()
# relRatio = changes.loc[:, 0].div(pop.loc[:, 0])
# print(relRatio)
pubSchools = publicSchoolsAvgGrowth(minStudents)
print(pubSchools)

for i in range(2007, 2017):
    stat, pval = stats.ttest_ind(pubSchools['GrowthIn' + str(i)], relSchools['GrowthIn' + str(i)])
    print('stat={}; pval={}'.format(stat, pval))

# pubSchools.index = pubSchools.index.map(str)
# pop = pubSchools.loc[[str(i) for i in range(2006, 2016)]].reset_index()
# changes = pubSchools.loc[['ChangeFrom{}To{}'.format(str(i), str(i+1)) for i in range(2006, 2016)]].reset_index()
# pubRatio = changes.loc[:, 0].div(pop.loc[:, 0])
# years = list(range(2007, 2017))
# plt.plot(years, relRatio, label='Religious Schools')
# plt.plot(years, pubRatio, label='public schools')
# plt.legend()
# plt.show()

# PERSISTED_FILE_FOR_PUBLIC = './data/generated/public-schools-combined-{}.csv'.format(int(tm.time()))
# PERSISTED_FILE_FOR_RELIGIOUS = './data/generated/religious-schools-combined-{}.csv'.format(int(tm.time()))
# schools.to_csv(PERSISTED_LIST_FILE, header=True, index=True)
