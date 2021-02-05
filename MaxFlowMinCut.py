#!/MinOddPath/venv/bin python3.6
# -*- coding: utf-8 -*-
from collections import defaultdict


def create_graph():
    num_vertices, num_edges = (map(int, input().split(" ")))
    vertices = set(range(1, num_vertices + 1))
    edges = defaultdict(list)

    while True:
        try:
            u, v = (map(int, input().split(" ")))
            add_edge(u, v, edges)
        except EOFError:
            break

    return vertices, edges


# Storing the weights with a dict. The key is a -> b. Value is the weight himself
def add_edge(u, v, edges):
    edges[u].append(v)
    edges[v].append(u)


def add_weighted_edge(u, v, wedges, weights, w):
    # This method is because now our graoh is directed
    wedges[u].append(v)
    weights[u, v] = w


def isBipartite(vertex, edges, color):
    # The color array store colors assigned to all vertices. Vertex number is used as index in this array.
    # If we don't have assigned a color yet, the value in the index of that vertex is -1.
    # -1 indicate first color, 2 indicate second.

    # Enqueue source = 1 for BFS traversal
    stack = [vertex]

    while stack:
        u = stack.pop()

        # Prevents self-loop
        if u in edges[u]:
            return False

        for v in edges[u]:
            if color[v] == -1:
                color[v] = 1 - color[u]
                stack.append(v)
            elif color[v] == color[u]:
                return False
    return True


def coloring_graph(vertices, edges):
    color = [-1] * (len(vertices) + 1)
    for v in range(1, len(vertices) + 1):
        if color[v] == -1:
            if not isBipartite(v, edges, color):
                return False
    return color if True else False


def create_bipartite(color, edges, source, sink):
    A = set()
    B = set()
    for i in range(len(color)):
        if color[i] == -1:
            A.add(i)
        else:
            B.add(i)
    A.remove(0)

    weights = {}
    wedges = defaultdict(list)
    netflow = [source]

    for u in A:
        add_weighted_edge(source, u, wedges, weights, w=1)
        add_weighted_edge(u, source, wedges, weights, w=0)
        netflow.append(u)
        for v in edges[u]:
            if v not in A:
                add_weighted_edge(u, v, wedges, weights, w=1)
                add_weighted_edge(v, u, wedges, weights, w=0)
    for u in B:
        add_weighted_edge(u, sink, wedges, weights, w=1)
        add_weighted_edge(sink, u, wedges, weights, w=0)
        netflow.append(u)
    netflow.append(sink)

    return netflow, wedges, weights, A, B


# This is based on the implementation of the CLRS book.
# The ford-fulkerson algorithm needs to run BFS to find the augmentation path.
def BFS(source, sink, parent, wedges, weights):
    visited = [False] * (sink + 1)
    stack = [source]
    visited[source] = True

    while stack:
        u = stack.pop(0)

        for v in wedges[u]:
            if not visited[v] and weights[u, v] > 0:
                visited[v] = True
                parent[v] = u
                stack.append(v)

    # This 'return' means that we have a path between source and sink, founded by BFS
    return True if visited[sink] else False


# We run BFS to find the residual graph's in the original graph
# After that, we remove the problem of antiparallel edges by incresing one and decresing the other
def find_minCut(vertices, wedges, weights, source, sink):
    num_vertices = len(vertices)
    parent = [-1] * (sink + 1)
    maximum_flow = 0

    while BFS(source, sink, parent, wedges, weights):
        flow = float('infinity')
        v = sink
        while v != source:
            flow = min(flow, weights[parent[v], v])
            v = parent[v]

        maximum_flow += flow
        v = sink
        while v != source:
            u = parent[v]
            weights[u, v] -= flow
            weights[v, u] += flow
            v = parent[v]

    couting_edges(A, B, weights)


# In this method, we run DFS in the final residual graph founded by BFS.
# We use this to find the edges used by the graph. This represents the cut.
def couting_edges(A, B, weights):
    answer = 0

    for k, v in weights.items():
        if k[0] in A and k[1] in B and weights[k[0], k[1]] == 0:
            answer += 1

    print(answer)


if __name__ == "__main__":
    vertices, edges = create_graph()
    colors = coloring_graph(vertices, edges)
    netflow, wedges, weights, A, B = create_bipartite(colors, edges, source=0, sink=len(vertices) + 1)
    find_minCut(netflow, wedges, weights, source=0, sink=len(vertices) + 1)
