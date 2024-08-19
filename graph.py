# Location is a vertex in the graph
# label is the locations address
# distance and prev_location are used for finding the shortest path with dijkstra's algorithm
# this vertex object supports dijkstra's algorithm but this solution does not use it
class Location:
    def __init__(self, address):
        self.address = address
        self.distance = float('inf')
        self.prev_location = None


# a representation of the graph data structure
# can be used as a weighted directed or undirected graph
# this program uses this graph solely as a weighted undirected complete graph
class Graph:
    def __init__(self):
        self.adjacent_locations = {}
        self.distances = {}

    # add a new vertex to the graph
    # create a list for the vertex to hold it's neighbors
    def add_location(self, new_location):
        self.adjacent_locations[new_location] = []

    # add a directed edge between one vertex and another
    def add_arc(self, from_location, to_location, distance):
        self.adjacent_locations[from_location].append(to_location)
        self.distances[(to_location, from_location)] = distance

    # create 2 directed edges between one vertex and another
    # effectively creating 1 undirected edge between the two
    def add_line(self, from_location, to_location, distance):
        self.add_arc(from_location, to_location, distance)
        self.add_arc(to_location, from_location, distance)
