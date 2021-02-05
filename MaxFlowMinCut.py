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


def add_weighted_edge(u, v, wedges, weights):
    # This method is because now our graoh is directed
    wedges[u].append(v)
    weights[u, v] = 1


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
        add_weighted_edge(source, u, wedges, weights)
        netflow.append(u)
        for v in edges[u]:
            add_weighted_edge(u, v, wedges, weights)
    for u in B:
        add_weighted_edge(u, sink, wedges, weights)
        netflow.append(u)
    netflow.append(sink)

# # This is based on the implementation of the CLRS book.
# # The ford-fulkerson algorithm needs to run BFS to find the augmentation path.
# def BFS(source, sink, parent, edges, weights):
#     visited = [False] * (source + 1)
#     stack = [source]
#     visited[source] = True
#
#     while stack:
#         u = stack.pop(0)
#         for v in edges[u]:
#             if not visited[v] and weights[u, v] > 0:
#                 visited[v] = True
#                 parent[v] = u
#                 stack.append(v)
#
#     # This 'return' means that we have a path between source and sink, founded by BFS
#     return True if visited[sink] else False
#
#
# # The DFS method is used to search for the path in residual graph
# def DFS(source, visited, num_vertices, edges):
#     visited[source] = True
#
#     for v in range(num_vertices):
#         if v in edges[source] and not visited[v]:
#             DFS(v, visited, num_vertices, edges)
#
#
# # We run BFS to find the residual graph's in the original graph
# # After that, we remove the problem of antiparallel edges by incresing one and decresing the other
# def find_minCut(source, sink, vertices, edges, weights):
#     num_vertices = len(vertices)
#     parent = [-1] * (source + 1)
#     maximum_flow = 0
#
#     while BFS(source, sink, parent, edges, weights):
#         flow = float('infinity')
#         vertex = sink
#         while vertex != source:
#             flow = min(flow, weights[parent[vertex], vertex])
#             vertex = parent[vertex]
#
#         maximum_flow += flow
#         vertex = sink
#
#         while vertex != source:
#             u = parent[vertex]
#             weights[u, vertex] -= flow
#             weights[vertex, u] += flow
#             vertex = parent[vertex]
#
#     apply_dfs(source, num_vertices, edges, weights)
#
#
# # In this method, we run DFS in the final residual graph founded by BFS.
# # We use this to find the edges used by the graph. This represents the cut.
# def apply_dfs(source, num_vertices, edges, weights):
#     visited = (num_vertices + 1) * [False]
#     DFS(source, visited, num_vertices, edges)
#
#     answer = 0
#     for u in range(num_vertices):
#         for v in edges[u]:
#             if weights[u, v] == 0 and visited[u]:
#                 answer += 1
#
#     print(answer)
if __name__ == "__main__":
    vertices, edges = create_graph()
    colors = coloring_graph(vertices, edges)
    create_bipartite(colors, edges, source=0, sink=len(vertices) + 1)

    # isBipartite(vertices, edges)
    # find_minCut(len(vertices), 1, vertices, edges, weights)
