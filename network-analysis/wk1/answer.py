from functools import reduce
import numpy as np
import pandas as pd
import networkx as nx
from networkx.algorithms import bipartite
import matplotlib.pyplot as plt

def data():
    # This is the set of employees
    employees = set(['Pablo',
                     'Lee',
                     'Georgia',
                     'Vincent',
                     'Andy',
                     'Frida',
                     'Joan',
                     'Claude'])

    # This is the set of movies
    movies = set(['The Shawshank Redemption',
                  'Forrest Gump',
                  'The Matrix',
                  'Anaconda',
                  'The Social Network',
                  'The Godfather',
                  'Monty Python and the Holy Grail',
                  'Snakes on a Plane',
                  'Kung Fu Panda',
                  'The Dark Knight',
                  'Mean Girls'])
    return employees, movies

# you can use the following function to plot graphs
# make sure to comment it out before submitting to the autograder
def plot_graph(G, weight_name=None):
    '''
    G: a networkx G
    weight_name: name of the attribute for plotting edge weights (if G is weighted)
    '''
    plt.figure()
    pos = nx.spring_layout(G)
    edges = G.edges()
    weights = None

    if weight_name:
        weights = [int(G[u][v][weight_name]) for u, v in edges]
        labels = nx.get_edge_attributes(G, weight_name)
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels)
        nx.draw_networkx(G, pos, edges=edges, width=weights)
    else:
        nx.draw_networkx(G, pos, edges=edges)
    plt.show(block=False)

def q1():
    return nx.read_adjlist('Employee_Movie_Choices.txt', nodetype=str, delimiter='\t')

def reduce_agg(acc_type: str):
    def temp(acc, curr: str):
        acc[curr] = {'type': acc_type} # for nx.__version__ < 2, acc[curr] = acc_type
        return acc
    return temp

def q2(employees, movies, G):
    attr = reduce(reduce_agg('employee'),
                  employees,
                  reduce(reduce_agg('movie'), movies, {}))
    nx.set_node_attributes(G, attr)
    return G

def q3(B: nx.Graph, employees: set):
    return bipartite.weighted_projected_graph(B, employees)

def q4(P: nx.Graph):
    '''
    P: weighted projection graph which tells us how many movies different pairs of employees have in common.
    '''
    rel_df = pd.read_csv('Employee_Relationships.txt', delim_whitespace=True, header=None, names=['n1', 'n2', 'weight'])
    emp_df = nx.to_pandas_dataframe(P).unstack().reset_index().query('level_0 != level_1').reset_index(drop=True)
    df = pd.merge(rel_df, emp_df, how='left', right_on=['level_0', 'level_1'], left_on=['n1', 'n2']).loc[:, ['weight', 0]]
    df.columns = ['relationship_score', 'num_movies_common']
    return df.corr().iloc[0, 1]

def execute_q4():
    employees, _ = data()
    return q4(q3(q1(), employees))
