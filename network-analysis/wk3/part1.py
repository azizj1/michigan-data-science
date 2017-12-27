import networkx as nx

def data():
    return nx.read_gml('friendships.gml')

def q1(G):
    return \
        nx.degree_centrality(G)[100], \
        nx.closeness_centrality(G)[100], \
        nx.betweenness_centrality(G, normalized=True, endpoints=False)[100]

def q2(G):
    return max(nx.degree_centrality(G).items(), key=lambda n: n[1])

def q3(G):
    return max(nx.closeness_centrality(G).items(), key=lambda n: n[1])

def q4(G):
    return max(nx.betweenness_centrality(G, normalized=True, endpoints=False).items(), key=lambda n: n[1])
