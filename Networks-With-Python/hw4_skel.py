# hw4_skel.py
# Joshua Reed
# 4/10/2019
  
import matplotlib.pyplot as plt
import networkx as nx
import numpy as np # to fit a line
import random

def price_model(n, n0, c, r):
    """
    n: int, number of nodes in the network
    n0: int, number of nodes initially
    c: int, out-degree (every node joins the network with c outgoing stubs)
    r: int, "free" copies on the stubs list
    """
    # this is how to create a directed graph in networkx
    G = nx.DiGraph()

    # adding nodes 0,...,n0-1
    G.add_nodes_from(range(n0))

    # here is how you can add node attributes in networkx
    for i in range(n0):
        G.nodes[i]['date_of_birth'] = 0
        
    # now you need to add the rest of the n-n0 nodes and connect them
    # preferentially (like in Price's model)
    stubs = [] # list of stubs

    for node in G.nodes(): # iterate over the nodes in G
        for i in range(r): # iterate over the range of r
            stubs.append(node) # append node to stubs r times
            
    for t in range(n0, n): # iterate over the remaining nodes
        G.add_node(t) # add the new node
        G.nodes[t]['date_of_birth'] = t - n0 + 1 # set its DOB
        
        for i in range(c): # iterate over range of c
            rand_idx = random.randint(0, len(stubs) - 1) # generate a random index
            rand_node = stubs[rand_idx] # get the corresponding node
            
            while (G.has_edge(t, rand_node) or (t == rand_node)): # avoid bad edges
                rand_idx = random.randint(0, len(stubs) - 1) # generate a random index
                rand_node = stubs[rand_idx] # get the corresponding node
            
            G.add_edge(t, rand_node) # add the edge to G
            stubs.append(rand_node) # add the random node to the stubs list
        
        for i in range(r): # iterate over the range of r
            stubs.append(t) # append t to stubs r times
    
    return G # return the graph
    
def calc_ccdf(G):
    """
    G: nxDiGraph, directed graph
    returns: two lists x,y such that x[i] is a degree and y[i] is the fraction
    of nodes that have in-degree larger than x[i]
    """
    n = G.number_of_nodes()

    # this is how to get a list with all in-degrees in the network
    in_degs = dict(G.in_degree()).values()

    x = range(n) # x values are all possible degrees
    y = [0 for i in x] # for each x value, how many nodes have degree > x
    num_zeros = 0 # number of encountered values of zero in y
    
    for pos_deg in x: # iterate over the possible degrees
        counter = 0 # num of act_deg bigger than pos_deg
        
        for act_deg in in_degs: # iterate over the actual degrees
            if pos_deg < act_deg: counter += 1 # increment counter
        
        y[pos_deg] = (counter / float(n)) # add counter to y
        
        if y[pos_deg] == 0: num_zeros += 1 # if y is zero, increment zero counter
        if num_zeros >= 1000: break # if we have too many zeros, yeet
        
    return x, y # return the result

def random_growth_model(n, n0, c):
    """
    n: int, number of nodes in the network
    n0: int, number of nodes initially
    c: int, out-degree (every node joins the network with c outgoing stubs)
    """
    # create graph
    G = nx.DiGraph()

    # add n0 nodes initially
    G.add_nodes_from(range(n0))
            
    for t in range(n0, n): # iterate over the remaining nodes
        #for i in range(t - 1): # iterate over all previous nodes
            #G.nodes[i]['age'] += 1 # increment their age
        
        #G.add_node(t) # add the new node
        #G.nodes[t]['age'] = 0 # set its age to be 0
        
        for i in range(c): # iterate over range of c
            rand_idx = random.randint(0, len(G) - 1) # generate a random index
            
            while (G.has_edge(t, rand_idx) or (t == rand_idx)): # avoid bad edges
                rand_idx = random.randint(0, len(G) - 1) # generate a random index
            
            G.add_edge(t, rand_idx) # add the edge to G
    
    return G # return the graph
    
def price_no_growth(n, c, r):
    """
    n: int, number of nodes in the network
    c: int, out-degree (every node has c outgoing links)
    r: int, "free" copies on the stubs list
    """
    # create directed graph
    G = nx.DiGraph()

    # add all the nodes
    G.add_nodes_from(range(n))
    
    stubs = [] # list of stubs

    for node in G.nodes(): # iterate over the nodes in G
        for i in range(r): # iterate over the range of r
            stubs.append(node) # append node to stubs r times

    for link_count in range(c): # iterate over the range of c
        for node in G.nodes(): # iterate over G's nodes
            rand_idx = random.randint(0, len(stubs) - 1) # generate a random index
            rand_node = stubs[rand_idx] # get the corresponding node
            
            while (G.has_edge(node, rand_node) or
                (G.has_edge(rand_node, node)) or
                (node == rand_node)): # avoid bad edges
                rand_idx = random.randint(0, len(stubs) - 1) # generate a random index
                rand_node = stubs[rand_idx] # get the corresponding node
            
            G.add_edge(node, rand_node) # add the edge to G
            stubs.append(rand_node) # add the random node to the stubs list
    
    return G # return the graph
    
# problem 1: implement Price model
G = price_model(n=100000, n0=10, c=3, r=1)

print("FINISHED 1\n")

# problem 2: plot degree distribution
x, y = calc_ccdf(G)
plt.plot(x, y, 'o', alpha=0.8)
plt.xlabel('x')
plt.ylabel('Pr(k>x)')
plt.xscale('log')
plt.yscale('log')
plt.savefig('problem2.pdf')
plt.clf() # clean environment

# report slope
xfit = []
yfit = []
for i in range(len(x)):
    if x[i] >= 10 and x[i] <= 1000:
        xfit.append(np.log10(x[i]))
        yfit.append(np.log10(y[i]))
print("slope of CCDF", np.polyfit(xfit, yfit, 1)[0])

print("FINISHED 2\n")

# problem 3: correlation between age and degree

x = range(100000 - 10 + 1) # list of nodes age
y = [0 for i in x] # list of corresponding in-degrees

# now you need to fill in x and y
for i in range(len(G)):
    DOB = G.nodes[i]['date_of_birth']
    y[DOB] += G.in_degree(i)
    
# plot
plt.plot(x, y, 'o', alpha=0.8)
plt.xlabel('age')
plt.ylabel('in-degree')
plt.yscale('log')
plt.savefig('problem3.pdf')
plt.clf()

# print the average in-degree of 1000 oldest and youngest nodes
avg_oldest = 0
avg_youngest = 0

for i in y[0:1000]:
    avg_oldest += i

for i in y[-1000:]:
    avg_youngest += i

print("Average in-degree of 1000 oldest: " + str(avg_oldest / 1000.0))
print("Average in-degree of 1000 youngest: " + str(avg_youngest / 1000.0))

pairs = []
counter = 10

for i, j in zip(x, y):
    pairs.append((i, j))

pairs.sort(key = lambda tup: tup[1])

for i in pairs[-10:]:
    print("Highest degree " + str(counter) + ": node" +
          str(i[0]) + " with degree " + str(i[1]))
    counter -= 1

print("FINISHED 3\n")


# problem 4: random growth model
G = random_growth_model(n=100000, n0=10, c=3)

x, y = calc_ccdf(G)
plt.plot(x, y, 'o', alpha=0.8)
plt.xlabel('x')
plt.ylabel('Pr(k>x)')
plt.xscale('log')
plt.yscale('log')
plt.savefig('problem4.pdf')
plt.clf()

print("FINISHED 4\n")

# problem 5: preferential attachment, no growth
G = price_no_growth(n=100000, c=3, r=1)
x, y = calc_ccdf(G)
plt.plot(x, y, 'o', alpha=0.8)
plt.xlabel('x')
plt.ylabel('Pr(k>x)')
plt.xscale('log')
plt.yscale('log')
plt.savefig('problem5.pdf')
plt.clf()

print("FINISHED 5\n")

