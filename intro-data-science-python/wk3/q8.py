import q1

def answer():
    top15 = q1.answer()
    top15['pop'] = top15['Energy Supply'] / top15['Energy Supply per Capita']
    largest = top15['pop'].nlargest(3)
    return largest.index[2]
print(answer())
