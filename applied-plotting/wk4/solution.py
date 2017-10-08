import time as tm
import privateSchools as priv
import publicSchools as pub
import religiousSchools as rel
import pandas as pd

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 150)

PERSISTED_LIST_FILE = './data/generated/public-schools-combined-{}.csv'.format(int(tm.time()))

publicSchools = pub.getSchools()
privateSchools = priv.getSchools()
religiousSchools = rel.getSchools()
print(publicSchools.shape)
print(privateSchools.shape)
print(religiousSchools.shape)
publicSchools.to_csv(PERSISTED_LIST_FILE, header=True, index=True)
