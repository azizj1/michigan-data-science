import networkx as nx

def q1():
    return nx.read_edgelist('email_network.txt', create_using=nx.MultiDiGraph(), nodetype=str, data=[('time', int)])

def q2(G):
    return len(G.nodes()), len(G.edges())

def q3(G):
    return nx.is_strongly_connected(G), nx.is_weakly_connected(G)

def q4(G):
    return len(max(nx.weakly_connected_components(G), key=len))

def q5(G):
    return len(max(nx.strongly_connected_components(G), key=len))

def q6(G):
    return max(nx.strongly_connected_component_subgraphs(G), key=lambda g: len(g.nodes()))

def q7(G_sc):
    return nx.average_shortest_path_length(G_sc)

def q8(G_sc):
    return nx.diameter(G_sc)

def q9(G_sc):
    return set(nx.periphery(G_sc))

def q10(G_sc):
    return set(nx.center(G_sc))

def q11(G_sc, nodes: set, min_distance: int):
    node_connections = [
        (
            node,
            list(filter(lambda v: v >= min_distance, nx.single_source_shortest_path_length(G_sc, node).values()))
        ) for node in nodes
    ]
    return max(node_connections, key=lambda n: len(n[1]))

def execute_q11():
    G_sc = q6(q1())
    max_connection = q11(G_sc, q9(G_sc), q8(G_sc))
    return max_connection

def q12(G_sc):
    src_nodes = q10(G_sc)
    dst_node = execute_q11()[0]
    return sum([nx.node_connectivity(G_sc, src_node, dst_node) for src_node in src_nodes])

def q13(G_sc):
    return nx.Graph(G_sc)

def q14(G_un):
    return nx.transitivity(G_un), nx.average_clustering(G_un)
