import q1

def answer():
    top15 = q1.answer()
    largest = top15['% Renewable'].nlargest(1)
    return (largest.index[0], largest.values[0])
