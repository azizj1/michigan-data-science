import part2a as p2a
import networkx as nx
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

def data():
    return pd.read_csv('future-connections.csv', index_col=0, converters={0: eval})

def classifier_data(df):
    G = p2a.data()
    df['c-neighbors'] = df.index.map(lambda n: len(list(nx.common_neighbors(G, n[0], n[1]))))
    df['pref-attach'] = [n[2] for n in nx.preferential_attachment(G, df.index)]
    return df[df['Future Connection'].isnull()], df[~df['Future Connection'].isnull()], G

def X_y(df):
    return df.filter(regex=r'^(?!Future Connection)'), df['Future Connection']

def learn(X, y):
    param_grid = {'C': list(range(10, 10, 100)) + list(range(100, 1001, 100))}
    clf = GridSearchCV(LogisticRegression(), param_grid=param_grid, cv=3, scoring='roc_auc', verbose=10).fit(X, y)
    print(clf.best_params_)
    print(clf.best_score_)
    return clf

def fit(X, y, C):
    return LogisticRegression(C=C).fit(X, y)

def predict(clf, df):
    X, _ = X_y(df)
    predictions = clf.predict_proba(X)
    return pd.Series(predictions[:, 1], index=X.index) # [:, 1] and not [:, 0] because clf.classes_

def execute():
    unknowns, train, _ = classifier_data(data())
    X, y = X_y(train)
    # C, = learn(X, y).best_params_.values()
    C = 100
    clf = fit(X, y, C)
    return predict(clf, unknowns)
