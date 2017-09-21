import q1

def answer():
    top15 = q1.answer()
    top15['pop'] = top15['Energy Supply'] / top15['Energy Supply per Capita']
    top15['docs per capita'] = top15['Citable documents'] / top15['pop']
    sigma = top15[['Energy Supply per Capita', 'docs per capita']].corr()
    return sigma.iloc[0,1]
print(answer())
