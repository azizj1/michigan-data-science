import networkx as nx
from scipy import stats

def data():
    return [nx.read_edgelist(f'graph{i}.edgelist') for i in range(0, 5)]

def is_pref_attachment(G):
    score = max(stats.zscore(list(map(lambda x: x[1], G.degree()))))
    return score > 8

def is_small_world_low_wiring_prob(G):
    avg_clustering = nx.average_clustering(G)
    return avg_clustering > 0.1

def is_small_world_high_wiring_prob(G):
    avg_clustering = nx.average_clustering(G)
    return avg_clustering <= 0.1

def graph_type(G):
    if is_pref_attachment(G):
        return 'PA'
    if is_small_world_low_wiring_prob(G):
        return 'SW_L'
    if is_small_world_high_wiring_prob(G):
        return 'SW_H'
    return 'SW_H'

def graph_identification():
    return [graph_type(G) for G in data()]
