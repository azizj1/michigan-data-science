import time as tm
import privateSchools as priv
import pandas as pd

pd.set_option('display.max_rows', 50)
pd.set_option('display.max_columns', 15)
pd.set_option('display.width', 150)

PERSISTED_LIST_FILE = './data/generated/private-schools-combined-{}.csv'.format(int(tm.time()))

schools = priv.getSchools()
print(schools)
# schools.to_csv(PERSISTED_LIST_FILE, header=True, index=True)
