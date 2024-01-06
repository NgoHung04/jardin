"""
Construct a graph from a csv file and apply Dijkstra algorithm
to find the shortest path between two vertices.
"""
import csv
import math


def construct_graph(file_path: str) -> dict:
    """
    Construct a graph from a csv file.
    :param file_path: path to the csv file
    :return: a dictionary of vertices and weights, dict[str, dict[str, int]]
    """
    with open(file_path, newline='') as csvfile:
        reader = csv.reader(csvfile, delimiter=';')
        # We get the vertices with keyword 'favorise'
        graph = {}
        for row in reader:
            if row[1] != 'favorise':
                continue
            try:
                graph[row[0]]
            except KeyError:
                graph[row[0]] = {}
            graph[row[0]][row[2]] = int(row[3])
    return graph


def get_all_vertices(graph: dict) -> list:
    """
    Get all vertices from a graph.
    :param graph: a graph, dict[str, dict[str, int]]
    :return: a list of vertices, list[str]
    """
    return list(graph.keys())


def release_arc(start_vertex: str, end_vertex: str, parent: dict, distance: dict, graph: dict):
    """
    Release an arc.
    :param start_vertex: start vertex, str
    :param end_vertex: end vertex, str
    :param parent: parent dictionary, dict[str, str]
    :param distance: distance dictionary, dict[str, int]
    :param graph: graph, dict[str, dict[str, int]]
    :return: None
    """
    try:
        distance[end_vertex]
    except KeyError:
        distance[end_vertex] = math.inf
    if distance[end_vertex] > distance[start_vertex] + graph[start_vertex][end_vertex]:
        distance[end_vertex] = distance[start_vertex] + graph[start_vertex][end_vertex]
        parent[end_vertex] = start_vertex


def dijkstra(start_vertex: str, graph: dict) -> tuple:
    """
    Dijkstra algorithm.
    :param start_vertex: start vertex, str
    :param graph: graph, dict[str, dict[str, int]]
    :return: a tuple of parent dictionary and distance dictionary, tuple[dict[str, str], dict[str, int]]
    """
    # Initialization
    parent = {}
    distance = {}
    white = []
    grey = []
    black = []
    for vertex in get_all_vertices(graph):
        white.append(vertex)
        parent[vertex] = None
        distance[vertex] = math.inf
    distance[start_vertex] = 0
    grey.append(start_vertex)
    white.remove(start_vertex)
    # Main loop
    while len(grey) > 0:
        # Find the vertex with the shortest distance
        min_distance = math.inf
        min_vertex = ''
        for vertex in grey:
            if distance[vertex] < min_distance:
                min_distance = distance[vertex]
                min_vertex = vertex
        # Release the vertex
        grey.remove(min_vertex)
        black.append(min_vertex)
        # Release all arcs from the vertex
        for vertex in graph[min_vertex].keys():
            release_arc(min_vertex, vertex, parent, distance, graph)
            if vertex in white:
                white.remove(vertex)
                grey.append(vertex)
    return parent, distance


if __name__ == '__main__':
    file_path = './data_arcs_poids.csv'
    graph = construct_graph(file_path)
    start_vertex = 'agrume'
    parent, distance = dijkstra(start_vertex, graph)
    print("Dijkstra algorithm result:")
    print("Parent dictionary:")
    print(parent)
    print("Distance dictionary:")
    print(distance)
