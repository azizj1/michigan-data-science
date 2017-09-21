import q1
import numpy as np

def continentDict():
    return  {'China':'Asia',
             'United States':'North America',
             'Japan':'Asia',
             'United Kingdom':'Europe',
             'Russian Federation':'Europe',
             'Canada':'North America',
             'Germany':'Europe',
             'India':'Asia',
             'France':'Europe',
             'South Korea':'Asia',
             'Italy':'Europe',
             'Spain':'Europe',
             'Iran':'Asia',
             'Australia':'Australia',
             'Brazil':'South America'}

def answer():
    top15 = q1.answer()
    continents = continentDict()
    top15['pop'] = top15['Energy Supply'] / top15['Energy Supply per Capita']
    desc = top15['pop'] \
            .groupby(lambda country: continents[country]) \
            .agg({'size': np.count_nonzero, 'sum': np.sum, 'mean': np.average, 'std': np.std})
    desc.index.name = 'Continent'
    return desc
