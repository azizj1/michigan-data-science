import numpy as np
from matplotlib import pyplot as plt, ticker as ticker

np.random.seed(12345)
means = [32000, 43000, 43500, 48000]
spreads = [200000, 100000, 140000, 70000]
size = 3650
tscoreAt95 = 1.96
marginErr = tscoreAt95 * np.array(spreads) / (size**(1/2))
years = list(range(1992, 1996))

def getColor(meanMarginPair, threshold):
    mean = meanMarginPair[0]
    err = meanMarginPair[1] / 2
    if mean + err < threshold:
        return 'blue'
    elif mean - err > threshold:
        return 'red'
    else:
        return 'gray'

def plotBars(x, y, err, threshold):
    colors = [getColor(p, threshold) for p in zip(y, err)]
    plt.bar(x, y, yerr=err, capsize=5, color=colors, alpha=0.8)
    plt.xticks(x)
    plt.axhline(y=threshold, color='gray', linestyle='-', alpha=0.5)
    plt.text(x[0] - 0.5, threshold + 200, 'y = {:,.0f}'.format(threshold), color='black', alpha=0.8)

def stylePlot():
    plt.gca().yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:,.0f}'.format(y)))
    for spine in plt.gca().spines.values():
        spine.set_visible(False)
    plt.tick_params(
        # axis='x', # changes apply to the x-axis
        which='both', # both major and minor ticks are affected
        bottom='off', # ticks along the bottom edge are off
        top='off', # ticks along the top edge are off,
        left='off',
        labelbottom='on', # labels along the bottom edge are off
        labelleft='on'
    )

plotBars(years, means, marginErr, 42000)
stylePlot()
plt.show()
