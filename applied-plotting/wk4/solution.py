import time as tm
import publicSchools as pub
import pandas as pd

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 10)
pd.set_option('display.width', 150)

PERSISTED_LIST_FILE = './data/generated/public-schools-combined-{}.csv'.format(int(tm.time()))

schools = pub.getSchools()
schools.to_csv(PERSISTED_LIST_FILE, header=True, index=True)
print(schools)
