import numpy as np
import q1

def getGdpColumns():
    return ['{}'.format(n) for n in np.arange(2006, 2016, 1)]

def answer():
    avgGDP = q1.answer()
    columns = getGdpColumns()
    avgGDP = avgGDP[columns].mean(1).sort_values(ascending=False)
    return avgGDP
