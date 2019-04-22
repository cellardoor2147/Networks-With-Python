# hw1_skel.py
# Saray Shai
# Feb 1, 2019

def BFS(graph, source):
    
    visited = {}
    distances = {}
    
    visited[str(source)] = True
    distances[str(source)] = 0

    next_nodes = [ (source,0) ]

    while len(next_nodes) > 0:

        curr_node, curr_dist = next_nodes.pop(0)

        for nei in graph.get_neighbors(curr_node):
            if not str(nei) in visited:
                visited[str(nei)] = True
                distances[str(nei)] = curr_dist + 1
                next_nodes.append((nei,curr_dist+1))
    return distances

def largest(obj):
    """
    obj = positive int object
    result = largest int definition in obj
    """
    largest = 0
    
    for elem in obj:
        value = int(obj.get(elem))
        if largest < value:
            largest = value

    return largest

class Graph(object):
    """
    Represents a graph with adj list
    """
    def __init__(self):
        self.nodes = {} #keys are nodes, values are lists of neighbors

    def len(self):
        return len(self.nodes)

    def is_edge(self, i, j):
        """
        i, j: node labels
        return: bool, True if the edge (i, j) exists and False otherwise
        """
        if (not str(i) in self.nodes) or (not str(j) in self.nodes):
            return False
        
        return j in self.nodes[str(i)]

    def add_edge(self, i, j):
        if not self.is_edge(i, j):
            if not str(i) in self.nodes:
                self.nodes[str(i)] = [j]
            else:
                self.nodes[str(i)].append(j)

            if not str(j) in self.nodes:
                self.nodes[str(j)] = [i]
            else:
                self.nodes[str(j)].append(i)

    def remove_edge(self, i, j):
        if self.is_edge(i, j):
            self.nodes[str(i)].remove(j)
            self.nodes[str(j)].remove(i)

    def get_neighbors(self, i):
        return self.nodes[str(i)]

    def get_degree(self, i):
        return len(self.get_neighbors(i))

    def av_nei_degree(self, i):
        neighbors = self.get_neighbors(i)
        sum = 0

        if len(neighbors) == 0:
            return 0
        
        for node in neighbors:
            sum += self.get_degree(node)

        return sum / len(neighbors)

print("Joshua Reed")
print("2/9/2019")
print("Professor Shai")
print("HW1 Code \n")

for net_id in ['0', '107', '348', '414', '686', '698', '1684', '1912', '3437', '3980']:

    # read data
    edge_list = []
    graph = Graph()
    
    fh = open('facebook/' + net_id + '.edges', 'r')
    for line in fh:
        line = line[:-1]
        line = line.split(" ")
        node1 = int(line[0])
        node2 = int(line[1])
        edge_list.append((node1,node2))
        graph.add_edge(node1, node2)
    fh.close()

    diameter = 0
    friendParadox = 0

    for node in graph.nodes:
        local_diameter = largest(BFS(graph, int(node)))

        if int(local_diameter) > int(diameter):
            diameter = local_diameter

        if graph.get_degree(node) < graph.av_nei_degree(node):
            friendParadox += 1
    
    # compute: number of nodes, number of edges, diameter, number of nodes with
    # degree < average degree of neighbors
    print("Network ID: " + net_id)
    print("Number of nodes: " + str(graph.len()))
    print("Number of edges: " + str(len(edge_list)))
    print("Diameter: " + str(diameter))
    print("Friendship paradox count: " + str(friendParadox) + "\n")


print("TESTS")
x = Graph()
x.add_edge(1, 2)
x.add_edge(1, 3)
x.add_edge(1, 4)
x.add_edge(3, 0)
x.add_edge(4, 5)
x.add_edge(5, 6)
x.add_edge(6, 7)
