from matplotlib import pyplot as plt, ticker
import seaborn as sns

def stylePlot(fig, ax1, ax2, ax3, pubBox, relBox, idxHighlight):
    hightlight = '#d62728'
    ax1.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:.0f}%'.format(float(y) * 100)))
    ax3.yaxis.set_major_formatter(ticker.FuncFormatter(lambda y, _: '{:.0f}%'.format(float(y) * 100)))

    ax3.plot([], [], color=hightlight, label='Statistically Different') # force legend item to be added

    ax3.set_title('Average Growth')
    ax3.legend(bbox_to_anchor=(0.72, 1.35), loc='upper left')

    # for the box plots, show every other xaxis tick
    numOfXTicks = len(ax1.get_xticklabels())
    tickInterval = 3 if numOfXTicks % 3 == 9 else 2
    plt.setp(ax1.get_xticklabels(), visible=False)
    plt.setp(ax2.get_xticklabels(), visible=False)
    for label1, label2 in zip(ax1.xaxis.get_ticklabels()[::tickInterval], ax2.xaxis.get_ticklabels()[::tickInterval]):
        label1.set_visible(True)
        label2.set_visible(True)

    # Hide the right and top spines
    ax1.spines['right'].set_visible(False)
    ax1.spines['top'].set_visible(False)
    ax2.spines['right'].set_visible(False)
    ax2.spines['top'].set_visible(False)
    ax3.spines['right'].set_visible(False)
    ax3.spines['top'].set_visible(False)

    fig.subplots_adjust(hspace=0.4, top=0.83, bottom=0.05)
    fig.suptitle('High School Enrollment Changes in WI, USA')

    pubColor = ax3.get_lines()[0].get_color()
    relColor = ax3.get_lines()[1].get_color()

    for b in pubBox['boxes']:
        b.set_color(pubColor)
    for b in relBox['boxes']:
        b.set_color(relColor)
    for w in pubBox['whiskers']:
        w.set_color(pubColor)
    for w in relBox['whiskers']:
        w.set_color(relColor)
    for idx in idxHighlight:
        pubBox['boxes'][idx].set_color(hightlight)
        pubBox['whiskers'][idx*2].set_color(hightlight)
        pubBox['whiskers'][idx*2 + 1].set_color(hightlight)
        relBox['boxes'][idx].set_color(hightlight)
        relBox['whiskers'][idx*2].set_color(hightlight)
        relBox['whiskers'][idx*2 + 1].set_color(hightlight)

def plot(pubData, relData, yrsWithSignificantDif):
    fig = plt.figure()
    plt.style.use('seaborn-white')
    ax1 = plt.subplot2grid((2, 2), (1, 0))
    ax2 = plt.subplot2grid((2, 2), (1, 1), sharey=ax1)
    ax3 = plt.subplot2grid((2, 2), (0, 0), colspan=2)

    pubData.mean().plot(ax=ax3, label='Religious Schools')
    relData.mean().plot(ax=ax3, label='Public Schools')

    pubBox = pubData.plot.box(ax=ax1, showfliers=False, title='Religious Schools', return_type='dict')
    relBox = relData.plot.box(ax=ax2, showfliers=False, title='Public Schools', return_type='dict')

    idxOfDif = [pubData.columns.get_loc(str(yr)) for yr in yrsWithSignificantDif]
    stylePlot(fig, ax1, ax2, ax3, pubBox, relBox, idxOfDif)
    plt.show()
