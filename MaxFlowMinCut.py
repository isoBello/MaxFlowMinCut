#!/MinOddPath/venv/bin python3.6
# -*- coding: utf-8 -*-
from collections import defaultdict

graph = None


class Graph:
    def __init__(self, vertices):
        # Using a list of adjacency to represent the graph
        self.vertices = set(range(1, vertices + 1))
        self.edges = defaultdict(list)
        self.weights = {}

    def add_edge(self, u, v):
        # Storing the weights with a dict. The key is a -> b. Value is the weight himself
        self.edges[u].append(v)
        self.edges[v].append(u)

        self.weights[(u, v)] = 1
        self.weights[(v, u)] = 1


def create_graph():
    num_vertices, num_edges = (map(int, input().split(" ")))
    global graph
    graph = Graph(num_vertices)

    while True:
        try:
            u, v = (map(int, input().split(" ")))
            graph.add_edge(u, v)
        except EOFError:
            break


# This is based on the implementation of the CLRS book.
# The ford-fulkerson algorithm needs to run BFS to find the augmentation path.
def BFS(source, sink, parent):
    visited = [False] * sink
    stack = [source]
    visited[source] = True

    global graph

    while stack:
        u = stack.pop(0)
        for v in graph.edges[u]:
            if not visited[v]:
                stack.append(v)
                visited[v] = True
                parent[v] = u

    # This 'return' means that we have a path between source and sink, founded by BFS
    return True if visited[sink] else False


# The DFS method is used to search in traversal of the graph
def DFS(source, visited):
    global graph
    visited[source] = True
    for v in range(len(graph.vertices)):
        if v in graph.edges[s] and not visited[v]:
            DFS(v, visited)


def find_minCut(source, sink):
    global graph
    parent = [-1] * sink
    maximum_flow = 0

    while BFS(source, sink, parent):
        flow = float('infinity')
        vertex = sink
        while vertex != source:
            flow = min(flow, parent[vertex])
            vertex = parent[vertex]

        maximum_flow += flow
        vertex = sink
        while vertex != source:
            u = parent[vertex]
            graph.weight[u, vertex] -= flow
            graph.weight[vertex, u] += flow
            vertex = parent[vertex]

    visited = len(graph.vertices) * [False]
    DFS(source, visited)

    for u in range(len(graph.vertices)):
        for v in graph.edges[u]:
            if graph.weights[u, v] == 0 and visited[u]:
                print(str(u) + " - " + str(v))


if __name__ == "__main__":
    create_graph()
    s = 1; t = len(graph.vertices)
    find_minCut(s, t)
