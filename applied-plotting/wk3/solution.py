import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

np.random.seed(12345)
means = [32000, 43000, 43500, 48000]
spreads = [200000, 100000, 140000, 70000]
size = 3650
tscoreAt95 = 1.96
marginErr = tscoreAt95 * np.array(spreads) / (size**(1/2))
years = list(range(1992, 1996))

df = pd.DataFrame([np.random.normal(m, s, size) for m, s in zip(means, spreads)], index=years)
plt.bar(years, means, yerr=marginErr, capsize=5)
plt.xticks(years)
plt.show()
