from graph import *

# THIS IS NOT USED IN THE SOLUTION #
# PLEASE IGNORE #


# it is functional, just not used for anything
# it doesn't have much value in this scenario

# dijkstras algorithm takes a starting location and finds the shortest path
# to every other location in the graph from that starting location
def shortest_path(graph, start_location):
    unvisited_vertices = []

    #make a copy of the provided graph
    short_graph = graph

    # create a queue of unvisited locations
    for current_vertex in short_graph.adjacent_locations:
        unvisited_vertices.append(current_vertex)

    # process the start location first
    start_location.distance = 0

    # while there is still locations to visit, continue looping
    while len(unvisited_vertices) > 0:
        smallest_index = 0

        # finds the next location to create a path from
        for i in range(0, len(unvisited_vertices)):
            if unvisited_vertices[i].distance < unvisited_vertices[smallest_index].distance:
                smallest_index = i

        current_vertex = unvisited_vertices.pop(smallest_index)

        for adj_location in short_graph.adjacent_locations[current_vertex]:

            # create a path to a location that travels through a different location
            distance = short_graph.distances[(current_vertex, adj_location)]
            path_distance = current_vertex.distance + distance

            # check if this path is shorter than the distance between the 2 nodes directly
            # if it is then set prev_lcoation point in the vertex
            if path_distance < adj_location.distance:
                adj_location.distance = path_distance
                adj_location.prev_location = current_vertex

    return short_graph

# follows locations prev_location pointer until it reaches the starting location.
# returns the path of locations followed
# this path is the shortest path to the end point from the starting point
def path_locations(start_location, end_location):
    path_locations = []
    current_location = end_location
    while current_location is not start_location:
        path_locations.append(current_location)

    return path_locations
