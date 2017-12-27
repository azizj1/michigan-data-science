import networkx as nx

def data():
    return nx.read_gml('blogs.gml')

def q5(G):
    return nx.pagerank(G, alpha=0.85)['realclearpolitics.com']

def q6(G):
    return list(map(lambda n: n[0], sorted(nx.pagerank(G, alpha=0.85).items(), key=lambda n: n[1], reverse=True)))[:5]

def q7(G):
    scores = nx.hits(G)
    return scores[0]['realclearpolitics.com'], scores[1]['realclearpolitics.com']

def q8(G):
    scores = nx.hits(G)[0]
    return list(map(lambda n: n[0], sorted(scores.items(), key=lambda n: n[1], reverse=True)))[:5]

def q9(G):
    scores = nx.hits(G)[1]
    return list(map(lambda n: n[0], sorted(scores.items(), key=lambda n: n[1], reverse=True)))[:5]
