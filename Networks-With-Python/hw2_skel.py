# hw2_skel.py
# Saray Shai
# Feb 17, 2019

import scipy as sp
from scipy.sparse import linalg

import networkx as nx


# NOTE: YOU ARE ONLY ALLOWED TO USE NETWORKX TO CREATE THE GRAPHS
# AND EXTRACT NEIGHBORS. IF IN DOUBT ABOUT SOMETHING, PLEASE ASK ME

# ALLOWED METHODS:
# networkx.Graph() to create a graph
# networkx.add_node(i) to add a node with label i
# networkx.add_edge(i,j) to add an edge between node with label i and node with label j
# networkx.Graph.neighbors(i) to get a list of neighbors of node i 
# networkx.Graph.nodes() # to get a list of all nodes in a graph
# networkx.Graph.edges() # to get a list of all edges in a graph

def BFS(G, node):
    """
    G: Graph
    node: node
    return: map of distances using BFS
    """
    visited = {}
    distances = {}
    
    visited[node] = True
    distances[node] = 0

    next_nodes = [(node, 0)]

    while len(next_nodes) > 0:

        curr_node, curr_dist = next_nodes.pop(0)

        for nei in G.neighbors(curr_node):
            if not str(nei) in visited:
                visited[str(nei)] = True
                distances[str(nei)] = curr_dist + 1
                next_nodes.append((nei,curr_dist+1))
    
    return distances

def compute_dc(G):
    """
    G: Graph
    return: dict, a map between each node to its degree centrality
    """
    res = {} # dictionary to return
    max = 0 # maximum dc in network; helps with normalization
    
    for node in G: # loop through the graph
        degree = len(list(G.neighbors(node)))
        
        if degree > max: max = degree # keep track of maximum dc
        
        res[node] = degree # map each node to its dc
    
    if max != 0: # check if a maximum dc even exists; avoid div by zero
        for node, dc in res.items(): # loop through the result
            res[node] = round(float(dc) / max, 5) # normalize each definition
    
    return res # return the result

def compute_ec(G):
    """
    G: Graph
    return: dict, a map between each node to its eigenvector centrality
    values are rounded to 5 digits after the decimal point
    """
    n = len(G.nodes())

    # initial guess
    ec = {node: 1 for node in G.nodes() }

    # this is the maximum number of iterations we want to run
    # hopefully things will converge much faster
    for i in range(100):

        # new guess
        new_ec = ec.copy()

        # update
        for node in G.nodes():
            for nei in G.neighbors(node):
                new_ec[node] += ec[nei]

        # normalize
        sum_ecs = sum(new_ec.values())
        new_ec = {node: n*(new_ec[node] / sum_ecs) for node in G.nodes() }

        # calculate difference from previous solution
        diff = 0
        for node in G.nodes():
            diff += abs(ec[node] - new_ec[node])
        diff /= n

        # we have converged!
        if diff < 0.0001:
            break

        ec = new_ec.copy()

    
    return { node: round(new_ec[node],5) for node in G.nodes() }

def ec_helper(A):
    """
    A: adjacency matrix
    return: list with entries corresponding to the leading eigenvector of A
    """
    eigenvalue, eigenvector = linalg.eigs(A, k=1)
    largest = eigenvector.flatten().real
    norm = sp.sign(largest.sum())*sp.linalg.norm(largest)
    return list(map(float,largest/norm))

def compute_bc(G):
    """
    G: Graph
    return: dict, a map between each node to its betweenness centrality
    """
    nodes = G.nodes()
    bc = {node: 0 for node in nodes}
    
    for source in nodes:
        stack = []
        preds = [[] for w in nodes]
        sig = [0 for t in nodes]
        sig[source] = 1
        dist = [-1 for t in nodes]
        dist[source] = 0
        queue = []
        queue.append(source)
        
        while queue != []:
            v = queue.pop()
            stack.insert(0, v)
            
            for w in G.neighbors(v):
                if dist[w] < 0:
                    queue.insert(0, w)
                    dist[w] = dist[v] + 1
                
                if dist[w] == dist[v] + 1:
                    sig[w] += sig[v]
                    preds[w].append(v)
    
        delta = [0 for v in nodes]
    
        while stack != []:
            w = stack.pop(0)
        
            for v in preds[w]: 
                delta[v] += ((float(sig[v])/sig[w]) * (1 + delta[w]))
            
            if w != source:
                bc[w] += delta[w]
    
    return bc
        
def compute_hc(G):
    """
    G: Graph
    return: dict, a map between each node to its harmonic centrality
    values are rounded to 5 digits after the decimal point
    """
    nodes = G.nodes() # nodes in G
    n = float(len(nodes)) # number of nodes in G
    res = {} # dictionary to return
    max = 0 # maximum hc in network; helps with normalization
    
    for node in nodes: # loop through the nodes
        sumDist = 0 # sum of distances to all other nodes
        
        for key, distance in BFS(G, node).items(): # sum all distances
            if float(distance) != 0.0: # don't divide by zero
                sumDist += (1.0 / float(distance)) # add to the node's sum
        
        res[node] = (1 / (n - 1)) * sumDist # map each node to its hc
        if res[node] > max: max = res[node] # keep track of max hc
    
    for node, hc in res.items(): # loop through the map
        res[node] = round(hc / max, 5) # map each node to its hc

    return res #return the result

def is_connected(G):
    nodes = list(G.nodes()) # get the graph's nodes
    n = len(nodes) # number of graph's nodes
    node = nodes[0] # get first node (arbitrary)
    distances = BFS(G, node) # get the distances from node to all other nodes
    
    return len(distances) == n + 1 # make sure all nodes are reachable from node

def get_largest_key(d):
    """
    d: dict
    returns: a list with all keys corresponding to the largest value 
    """
    max_keys = []
    max_val = max(d.values())
    for k in d.keys():
        if d[k] == max_val:
            max_keys.append(k)
    return max_keys

def all_binary(n):
    """
    pre: n >= 0
    post: list of all binary string permutations of length n
    
    n: integer, >= 0
    """
    if (n == 1): return ["0", "1"] # base case
    
    res = [] # result
    rec = all_binary(n - 1) # recursive call

    for elem in rec: # loop through rec
        res.append(elem + "0") # append its element plus 0
        res.append(elem + "1") # append its element plus 1
    
    return res # return the result

def generateNetwork(s, n):
    """
    pre: true
    post: graph that corresponds s
    
    s: string, contains only 1's and 0's
    n: integer, >= 0
    """
    G = nx.Graph() # graph to return
    
    for i in range(0, n): # loop through nodes
        G.add_node(i) # add nodes to G
    
    for i in range(0, n): # loop through nodes
        for j in range(i + 1, n): # loop through i's possible neighbors
            if s[i + j - 1] == "1": G.add_edge(i, j) # add edges when needed
    
    return G # return the resulting graph, G

if __name__ == "__main__":
    # note that I removed the pair ('dc', 'hc') since it takes a really long
    # time. Try it if you like!
    
    for pair in [ ('dc','ec'), ('dc','bc'), ('ec','bc'), ('ec','hc'), ('hc','bc') ]:
        n = 2 
        found = False
        while not found and n < 10:
            print('trying n =',n, 'for', pair)

            # iterate over all possbile networks
            for s in all_binary(n * (n - 1) / 2):
                G = generateNetwork(s, n)

                # if G is not connected, continue to the next one
                if not is_connected(G):
                    continue
                
                # compute centralities
                c1 = compute_dc(G) #eval('compute_%s(G)'%pair[0])
                c2 = compute_bc(G) #eval('compute_%s(G)'%pair[1])

                # get highest centralities
                l1 = get_largest_key(c1)
                l2 = get_largest_key(c2)
 
                # check if there is more than one nodes with highest centrality
                if len(l1) > 1 or len(l2) > 1:
                    continue 
 
                if l1[0] != l2[0]:
                # found a network with different and distinct winners
                  print(pair)
                  print(n)
                # print the network adjacency matric
                  found = True
                  break
                
            n += 1
