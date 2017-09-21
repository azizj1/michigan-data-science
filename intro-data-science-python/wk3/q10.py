import q1

def answer():
    top15 = q1.answer()
    med = top15['% Renewable'].median()
    top15.loc[top15['% Renewable'] >= med, 'HighRenew'] = 1
    top15.loc[top15['% Renewable'] < med, 'HighRenew'] = 0
    return top15.sort_values('Rank')['HighRenew']
print(answer())
