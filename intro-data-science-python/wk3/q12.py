import q1
import q11
import pandas as pd
import numpy as np
def answer():
    top15 = q1.answer()
    top15['pop'] = top15['Energy Supply'] / top15['Energy Supply per Capita']
    top15['bucket'] = pd.cut(top15['% Renewable'], 5)
    continents = q11.continentDict()
    count = top15[['pop', 'bucket']] \
                .groupby([lambda country: continents[country], 'bucket']) \
                .count() \
                .dropna()
    count.index.rename(['Continent', 'bins'], inplace=True)
    count.columns = ['count']
    return pd.Series(count['count'], index=count.index)
print(type(answer()))
