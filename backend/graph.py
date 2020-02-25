repr = """
-------------------------------------------------------------------------------------
    Vertices: {}
    Edges: {}
-------------------------------------------------------------------------------------
"""
class Graph:
    
    def __init__(self, adj_list={}):
        self.adj_list = adj_list

    def __str__(self):
        v = list(self.vertices())
        e = self.edges()
        return repr.format(v, e)

    def vertices(self):
        return self.adj_list.keys()

    def edges(self):
        edges = []
        for vertex in self.adj_list:
            for neighbour in self.adj_list[vertex]:
                edges.append((vertex, neighbour))
        return edges

    def add_vertex(self, vertex):
        if vertex not in self.adj_list:
            self.adj_list[vertex] = []

    def add_edge(self, edge):
        (vertex1, vertex2) = tuple(edge)
        if vertex1 not in self.adj_list:
            raise KeyError
        if vertex2 not in self.adj_list:
            raise KeyError
        self.adj_list[vertex1].append(vertex2)

    def BFS(self, start):
        visited = [False] * (len(self.adj_list))
        visited[start] = True

        dist = [float("Inf")] * len(self.adj_list)
        dist[start] = 0

        pred = [None] * len(self.adj_list)

        queue = []
        queue.append(start)
        while queue:
            vertex = queue.pop(0)            
            for neighbor in self.adj_list[vertex]:
                if not visited[neighbor]:
                    queue.append(neighbor)
                    visited[neighbor] = True
                    dist[neighbor] = dist[vertex] + 1
                    pred[neighbor] = vertex

        return (dist, pred)

    def dijkstra(self, start, goal):
        heuristic = lambda vertex: 0
        return self.a_star(start, goal, heuristic)

    def a_star(self, start, goal, heuristic):
        dist = [float("Inf")] * len(self.adj_list)
        dist[start] = 0

        pred = [None] * len(self.adj_list)

        Q = []
        for vertex in self.adj_list:
            Q.append(vertex)

        while Q:
            _, vertex = min([(dist[el] + heuristic(el), el) for el in Q])
            if vertex == goal:
                break
            Q.remove(vertex)

            for neighbor in self.adj_list[vertex]:
                if dist[neighbor] > dist[vertex] + 1:
                    dist[neighbor] = dist[vertex] + 1
                    pred[neighbor] = vertex

        return (dist, pred)

    def get_path_length(self, start):
        path_length, _ = self.BFS(start)
        return path_length