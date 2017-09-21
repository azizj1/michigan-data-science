import q1
import q3

def answer():
    top15 = q1.answer()
    country = q3.answer().index[5]
    gdp2006 = top15.loc[country, '2006']
    gdp2015 = top15.loc[country, '2015']
    return gdp2015 - gdp2006
print(answer())
