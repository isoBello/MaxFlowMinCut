#!/MinOddPath/venv/bin python3.6
# -*- coding: utf-8 -*-
from collections import defaultdict


def create_graph():
    num_vertices, num_edges = (map(int, input().split(" ")))
    vertices = set(range(1, num_vertices + 1))
    edges = defaultdict(list)
    weights = {}

    while True:
        try:
            u, v = (map(int, input().split(" ")))
            add_edge(u, v, edges, weights)
        except EOFError:
            break

    return vertices, edges, weights


# Storing the weights with a dict. The key is a -> b. Value is the weight himself
def add_edge(u, v, edges, weights):
    edges[u].append(v)
    edges[v].append(u)

    weights[(u, v)] = 1
    weights[(v, u)] = 1


# This is based on the implementation of the CLRS book.
# The ford-fulkerson algorithm needs to run BFS to find the augmentation path.
def BFS(source, sink, parent, edges, weights):
    visited = [False] * (sink + 1)
    stack = [source]
    visited[source] = True

    while stack:
        u = stack.pop(0)
        for v in edges[u]:
            if not visited[v] and weights[u, v] > 0:
                visited[v] = True
                parent[v] = u
                stack.append(v)

    # This 'return' means that we have a path between source and sink, founded by BFS
    return True if visited[sink] else False


# The DFS method is used to search for the path in residual graph
def DFS(source, visited, num_vertices, edges):
    visited[source] = True

    for v in range(num_vertices):
        if v in edges[source] and not visited[v]:
            DFS(v, visited, num_vertices, edges)


def find_minCut(source, sink, vertices, edges, weights):
    num_vertices = len(vertices)
    parent = [-1] * (sink + 1)
    maximum_flow = 0

    while BFS(source, sink, parent):
        flow = 99999
        vertex = sink
        while vertex != source:
            flow = min(flow, weights[parent[vertex], vertex])
            vertex = parent[vertex]

        maximum_flow += flow
        vertex = sink

        while vertex != source:
            u = parent[vertex]
            weights[u, vertex] -= flow
            weights[vertex, u] += flow
            vertex = parent[vertex]

    apply_dfs(source, num_vertices, edges, weights)


# In this method, we run DFS in the final residual graph founded by BFS.
# We use this to find the edges used by the graph. This represents the cut.
def apply_dfs(source, num_vertices, edges, weights):
    visited = num_vertices * [False]
    DFS(source, visited, num_vertices, edges)

    answer = 0
    for u in range(num_vertices):
        for v in edges[u]:
            if weights[u, v] == 0 and visited[u]:
                answer += 1

    print(answer)


if __name__ == "__main__":
    vertices, edges, weights = create_graph()
    find_minCut(1, len(vertices), vertices, edges, weights)
