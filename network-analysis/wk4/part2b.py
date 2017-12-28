import part2a as p2a
import networkx as nx
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

def data():
    return pd.read_csv('future-connections.csv', index_col=0, converters={0: eval})

def classifier_data(df):
    G = p2a.data()
    return df[df['Future Connection'].isnull()], df[~df['Future Connection'].isnull()]
