import q1

def answer():
    top15 = q1.answer()
    top15['ratio'] = top15['Self-citations'] / top15['Citations']
    largest = top15['ratio'].nlargest(1)
    return (largest.index[0], largest.values[0])
print(answer())
