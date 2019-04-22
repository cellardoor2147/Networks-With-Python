# hw3_skel.py
# YOUR NAME
# DATE SUBMITTED

import networkx as nx
import random


# NOTE: please read this skeleton carefully since I changed some things from the written
# specification so that the code will take less time to run.

# ALSO, I advise you to process the collaboration network last (as it appears here) since
# it's taking the longest to run.

# Some useful random number functions:

# random.random(): random number uniformly at random from [0,1)

# random.sample(list, k): list of k elements chosen randomly from list

# random.sample(list, k): list of k elements chosen randomly from list

# random.shuffle(list): shuffles the list

# random.seed(int): initialize internal state of the random number generator. Useful for debugging.

def count_triangles(G):
    """
    G: networkx undirected simple Graph
    return: int, number of triangles in G
    """
    # don't use the networkx function that counts triangles!
    nodes = G.nodes()  # nodes in G
    res = 0 # number of triangles to return
    
    for i in nodes: # iterate through the nodes in i
        for j in G.neighbors(i): # iterate through i's neighbors
            for k in G.neighbors(j): # iterate through j's neighbors
                if G.has_edge(k, i): # check to see if i and k are connected
                    res += 1 # if so, add one to our result
    
    return res / 6 # divide by 3 to account for recounted triangles

def probabilisticBinary(p):
    """
    pre: 0.0 <= p <= 1.0
    post: a randomly generated binary digit, determined by p
    
    p: real, probability to return either 1 rathern than 0
    """
    rnd = random.random() # randomly generated number to compare to p
    
    return "0" if (rnd > p) else "1" # return 1 or 0 based on rnd

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

def create_ER_graph(n, p):
    """
    n: int, number of nodes
    p: float, edge probability
    return: networkx undirected simple Graph
    """
    s = "" # binary string to give to generateNetworks
    
    for i in range((n * (n - 1)) / 2): # loop through the upper-right triangle of the Adj. Mat.
        s += probabilisticBinary(p) # append either a 0 and 1 to our string
    
    return generateNetwork(s, n) # feed the string and graph size to generateNetworks

def create_configuration_graph(deg_seq):
    """
    deg_seq: list of integers
    return: networkx undirected simple Graph
    """
    G = nx.Graph() # graph to return
    n = len(deg_seq) # number of nodes in G
    v = [] # list of stubs
    
    for i in range(n): # iterate over the indices degree seq
        current = deg_seq[i] # store a copy of the current degree
        
        while current > 0: # while the current degree is over zero
            current -= 1 # decriment the current degree
            v.append(i) # append the index to our stubs list
    
    random.shuffle(v) # shuffle the stubs list
    
    for i in range(len(v)):  # iterate over the stubs list
        if i % 2 != 0: continue # skip odd elements
        if v[i] == v[i + 1]: continue # avoid self-loops
    
        G.add_edge(v[i], v[i + 1]) # add an edge between the current node and the next
    
    return G # return the graph
    
if __name__ == "__main__":

    for fn in ['celegans_n306', 'USairport_2010', 'USpowergrid_n4941', 'OClinks_w_chars', 'Newman-Cond_mat_95-99-binary']:
    
        # create graph
        G = nx.Graph()
    
        fh = open(fn  + '.txt', 'r') # open for read
        for line in fh:
            i = int(line.split(" ")[0])
            j = int(line.split(" ")[1])
            G.add_edge(i,j)
        fh.close() # close file handler
    
        # calculate number of nodes, edges and triangles
        n = len(G.nodes())
        m = len(G.edges())
        t = count_triangles(G)

        print(fn)
        print("# nodes", n)
        print("# edges", m)
        print("# triangles", t)
        
        res = 0 # result of adding ER triangles
        p = float(2 * m) / (n * (n - 1)) # probability of edges
    
        # create 10 G(n,p) graphs and report the average number of triangles
        for i in range(10): # do computation 10 times
            G_ER = create_ER_graph(n, p) # generate ER graph
            res += count_triangles(G_ER) # add triangles to result

        print("avg # triangles in ER", res // 10) # print result

        # create 10 configuration model graphs and report the average number of triangles
        deg_seq = [] # degree sequence
        res = 0 # result of adding CM triangles
        
        for node in G.nodes(): # iterate through G's nodes
            deg_seq.append(G.degree(node)) # add degrees to degree sequence
            
        for i in range(10): # do computation 10 times
            G_CM = create_configuration_graph(deg_seq) # generate CM graph
            res += count_triangles(G_CM) # add triangles to result
        
        print("avg # triangles in CM", res // 10) # print result

        # perform degree preserving rewiring m times and report number of
        # triangles after every 100 rewirings
        for i in range(m): # iterate over edges
            edges = list(G.edges()) # get the edges as a list
            (i0, j0) = edges[random.randint(0, len(edges) - 1)] # select random edge
            (i1, j1) = edges[random.randint(0, len(edges) - 1)] # select random edge
            
            while ((i0 in [i1, j1] and j0 in [i1, j1]) or # keep regenerating until we get a valid edge
                  (G.has_edge(i0, j1) or G.has_edge(i1, j0))):
                    (i0, j0) = edges[random.randint(0, len(edges) - 1)]
                    (i1, j1) = edges[random.randint(0, len(edges) - 1)]
        
            G.remove_edge(i0, j0) # remove the first edge
            G.remove_edge(i1, j1) # remove the second edge
            
            G.add_edge(i0, j1) # add a shuffled edge
            G.add_edge(i1, j0) # add a shuffled edge
            
            if i % 100 == 0: print("Rewiring at step", i, "with triangles", count_triangles(G)) # print result

        print("continuing to the next graph\n")