import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.max_colwidth', 250)
pd.set_option('display.width', 350)

def data():
    doc = []
    with open('dates.txt') as file:
        for line in file:
            doc.append(line)
    return pd.Series(doc)

def date_sorter(df):
    return df.str.extract(r'\b0?((?:([0-3]?\d)(?:[-/\s]|(?=[A-Z])))?[A-Za-z]?((?:Jan|Feb|Mar|Apr|May|Jun|Jul|Aug|Sep|Oct|Nov|Dec)[a-z,\.]*?[-/\s])?(?:([0-3]?\d)(?:st|nd|th)?,?[-/\s])?(?:s|y)?((?:(?:20|19)\d\d)|(?:(?<=/)\d\d)|(?:(?<=-\d-)\d\d)|(?:(?<=-\d\d-)\d\d)))\b')

def execute():
    s = data()
    df = date_sorter(s)
    merged = pd.merge(df, pd.DataFrame(s, columns=['Original']), left_index=True, right_index=True)
    print(merged)

execute()
