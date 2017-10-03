import numpy as np
from matplotlib import pyplot as plt, animation as animation, widgets as w

# generate 4 random variables from the random, gamma, exponential, and uniform distributions
x1 = np.random.normal(-2.5, 1, 10000)
x2 = np.random.gamma(2, 1.5, 10000)
x3 = np.random.exponential(2, 10000)+7
x4 = np.random.uniform(14, 20, 10000)
fig, ((ax1, ax2), (ax3, ax4)) = plt.subplots(2, 2, sharey=True)

n = 200
pointsShown = 0
binSizeAxes = plt.axes([0.15, 0.1, 0.65, 0.03])
binSlider = w.Slider(binSizeAxes, 'Bin Size', 100, 1000, valinit=n)

def updateBinSize(val):
    global n
    n = binSlider.val
binSlider.on_changed(updateBinSize)

def updateAnimation(curr):
    global pointsShown, n
    if pointsShown > 10000: # a hundred because we're goign to draw a 100 samples at a time, and 100*100 = n = 10k
        a.event_source.stop()
        return
    roundedN = int(n)
    pointsShown += roundedN
    ax1.cla()
    ax2.cla()
    ax3.cla()
    ax4.cla()
    ax1.set_title('x1\nNormal')
    ax2.set_title('x2\nGamma')
    ax3.set_title('x3\nExponential')
    ax4.set_title('x4\nUniform')
    # plot the histograms
    ax1.hist(x1[:pointsShown], bins=20, alpha=0.5, range=(-6,1))
    ax2.hist(x2[:pointsShown], bins=20, alpha=0.5, range=(-1, 15))
    ax3.hist(x3[:pointsShown], bins=20, alpha=0.5, range=(0, 20))
    ax4.hist(x4[:pointsShown], bins=20, alpha=0.5, range=(13, 21))
    ax1.set_xlim([-6, 1])
    ax1.set_ylim([0, 3000])
    ax2.set_xlim([-1, 15])
    ax2.set_ylim([0, 3000])
    ax3.set_xlim([0, 20])
    ax3.set_ylim([0, 3000])
    ax4.set_xlim([13, 21])
    ax4.set_ylim([0, 3000])

plt.subplots_adjust(hspace=0.5, bottom=0.25)
# plt.axis([-7,21,0,0.6])
a = animation.FuncAnimation(fig, updateAnimation, interval=100)
plt.show()
