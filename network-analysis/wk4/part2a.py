import pickle
import networkx as nx
import pandas as pd
from sklearn.linear_model import LogisticRegression
from sklearn.model_selection import GridSearchCV

def data():
    with open('email_prediction.pickle', 'rb') as input_file:
        nodes, edges = pickle.load(input_file)
        G = nx.Graph()
        G.add_nodes_from(nodes)
        G.add_edges_from(edges)
        return G

def clasifier_data(G):
    df = pd.DataFrame(index=G.nodes())
    df['department'] = pd.Series(nx.get_node_attributes(G, 'Department'))
    df['managementsalary'] = pd.Series(nx.get_node_attributes(G, 'ManagementSalary'))
    df['clustering'] = pd.Series(nx.clustering(G))
    df['degree'] = pd.Series(nx.degree_centrality(G))
    return df[df['managementsalary'].isnull()], df[~df['managementsalary'].isnull()]

def X_y(df):
    return df.filter(regex=r'^(?!managementsalary)'), df['managementsalary']

def learn(X, y):
    param_grid = {'C': [10, 20, 40, 60, 80] + list(range(100, 1001, 100))}
    clf = GridSearchCV(LogisticRegression(), param_grid=param_grid, cv=3, scoring='roc_auc', verbose=10).fit(X, y)
    print(clf.best_params_)
    return clf

def fit(X, y, C):
    return LogisticRegression(C=C).fit(X, y)

def predict(clf, df):
    X, _ = X_y(df)
    predictions = clf.predict_proba(X)
    return pd.Series(predictions[:, 1], index=X.index)  # [:, 1] and not [:, 0] because clf.classes_

def execute():
    unknowns, train = clasifier_data(data())
    X, y = X_y(train)
    # C, = learn(X, y).best_params_.values()
    C = 80
    clf = fit(X, y, C)
    return predict(clf, unknowns)
