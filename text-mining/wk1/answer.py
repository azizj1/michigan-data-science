from datetime import date
import re
import pandas as pd
import numpy as np

def data():
    doc = []
    with open('dates.txt') as file:
        for line in file:
            doc.append(line)
    return pd.Series(doc)

def to_date(s):
    year = s[4]
    month = 1
    day = 1
    if s[2] > 0: # jan, feb, .. converted to 1-12
        month = s[2]
        day = max(s[1], s[3], 1) # 1 in case there are no days
    elif s[1] < 0 or s[3] < 0: # means one of them is a month, the other is no date (day = 1)
        month = max(s[1], s[3], 1)
        day = 1
    else:
        month = s[1]
        day = s[3]
    if re.match(r'^\d\d[\s,]+\d\d\d\d$', s[0]) is not None: # cases where we were getting "16, 1976" or "19, 1988"
        day = 1
        month = 1
    return pd.Series({0: s[0], 1: s[1], 2: s[2], 3: s[3], 4: s[4], 'date': date(year, month, day)})

def date_sorter(df):
    return df.str.extract(r'\b0?((?:([0-3]?\d)(?:[-/\s]|(?=[A-Z])))?[A-Za-z]?((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z,\.]*?[-/\s])?(?:([0-3]?\d)(?:st|nd|th)?,?[-/\s])?(?:s|y)?((?:(?:20|19)\d\d)|(?:(?<=/)\d\d)|(?:(?<=-\d-)\d\d)|(?:(?<=-\d\d-)\d\d)))\b') \
                .replace({4: {r'^(\d\d)$': r'19\1'}, 2: {r'^.*Jan.*$': 1, r'^.*Feb.*$': 2, r'^.*Mar.*$': 3, r'^.*Apr.*$': 4, r'^.*May.*$': 5, r'^.*Jun.*$': 6, r'^.*Jul.*$': 7, r'^.*Aug.*$': 8, r'^.*Sep.*$': 9, r'^.*Oct.*$': 10, r'^.*Nov.*$': 11, r'^.*Dec.*$': 12}}, regex=True) \
                .fillna(-1) \
                .astype({1: np.int32, 2: np.int32, 3: np.int32, 4: np.int32}) \
                .apply(to_date, axis=1) \
                .sort_values(by='date')

def execute():
    s = data()
    return date_sorter(s).reset_index().iloc[:, 0]

execute()
