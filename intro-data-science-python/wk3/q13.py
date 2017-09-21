import q1

def answer():
    top15 = q1.answer()
    top15['pop'] = top15['Energy Supply'] / top15['Energy Supply per Capita']
    print(top15.loc['China','pop'])
    PopEst = top15['pop'].map('{:,}'.format)
    return PopEst
print(answer())
