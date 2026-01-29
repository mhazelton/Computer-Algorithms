"""
Max Hazelton
CISC-4080-R01
Lab 4, Graph Lab
"""

class Graph:
    def __init__(self, directed=False):
        self.directed = directed
        self.vertices = []  # list of vertices
        self.adj = {}       # dict: map vertex to adj list

        self.d = {}         # distance (hop count) from source in BFS
        self.pred = {}      # predecessor in BFS tree
        self.color = {}     # can be used for DFS / topo sort later
        self.pre_order = [] # DFS pre-order list
        self.post_order = []# DFS post-order list

    def add_vertex(self, v):
        if v not in self.vertices:
            self.vertices.append(v)
        if v not in self.adj:
            self.adj[v] = []

    def add_edge(self, u, v):
        self.add_vertex(u)
        self.add_vertex(v)
        self.adj[u].append(v)

        if not self.directed:
            self.adj[v].append(u)

    def initialize_from_file(self, file_name):
        print(f"Loading graph from {file_name}")
        self.vertices = []
        self.adj = {}

        try:
            f = open(file_name, "r")
        except IOError:
            print(f"Failed to open file {file_name}")
            raise

        word = f.readline().strip()
        if word.lower() == "true":
            self.directed = True
        elif word.lower() == "false":
            self.directed = False
        else:
            raise ValueError(f"Invalid directed flag: {word}")

        print(f"The graph is directed: {word}")

        # Read number of nodes
        line = f.readline().strip()
        node_num = int(line)
        print(f"With {node_num} nodes")

        # Read node list and initialize adjacency lists
        nodes = f.readline().split()
        for u in nodes:
            self.add_vertex(u)

        for line in f:
            parts = line.split()
            if len(parts) != 3:
                continue
            from_node, label, to_node = parts
            self.add_edge(from_node, to_node)

        f.close()

    def print(self):
        print("Vertices:")
        print(self.vertices)

        print("Adjacency lists:")
        # Iterate through all key value pair in the dict adj:
        for u, adjList in self.adj.items():
            print("Node ", u, "'s adjacency list:")
            print(adjList)

    def BFS(self, s):
        print("Perform a BFS from src node", s)

        # If source is not in the graph, just report and stop
        if s not in self.vertices:
            print("Source node", s, "is not in the graph.")
            return

        # Reset BFS-related data
        self.d = {}
        self.pred = {}

        visited = set()
        visited.add(s)

        self.d[s] = 0
        self.pred[s] = None

        Q = []          # list as queue
        Q.append(s)

        while len(Q) > 0:
            u = Q.pop(0)            # dequeue from front
            for v in self.adj[u]:   # neighbors of u
                if v not in visited:
                    visited.add(v)
                    self.d[v] = self.d[u] + 1
                    self.pred[v] = u
                    Q.append(v)

    # return the path in the format of a list of nodes, s, u, v, ... d
    # If there is no path from s to d, return an empty list
    def ShortestHopPath(self, s, d):
        print("Find shortest hop path from", s, "to", d)

        # If either node is not even in the graph, no path
        if s not in self.vertices or d not in self.vertices:
            return []

        # Run BFS from s to fill d[] and pred[]
        self.BFS(s)

        # If destination was not reached by BFS, no path
        if d not in self.d:
            return []

        # Reconstruct path by walking pred[] backwards from d to s
        path = []
        current = d
        while current is not None:
            path.append(current)
            current = self.pred[current]

        path.reverse()
        return path

    # -DFS implementation-

    # helper for DFS / DFS_Graph
    def _DFS_visit(self, u):
        # mark u as discovered
        self.color[u] = "gray"
        self.pre_order.append(u)

        # explore all neighbors
        for v in self.adj[u]:
            if self.color.get(v, "white") == "white":
                self._DFS_visit(v)

        # finished exploring u
        self.color[u] = "black"
        self.post_order.append(u)

    # perform a DFS traversal from node s, to reach all nodes
    # reachable from s
    def DFS(self, s):
        print("Perform a DFS from src node", s)

        if s not in self.vertices:
            print("Source node", s, "is not in the graph.")
            return

        self.color = {v: "white" for v in self.vertices}
        self.pre_order = []
        self.post_order = []

        # start DFS from s
        self._DFS_visit(s)

    # perform a complete DFS traversal
    def DFS_Graph(self):
        print("Perform a complete DFS")

        self.color = {v: "white" for v in self.vertices}
        self.pre_order = []
        self.post_order = []

        for v in self.vertices:
            if self.color[v] == "white":
                self._DFS_visit(v)

    # Check if a directed graph has cycle or not, and
    def DAG_TopoSort(self):
        print("DAG: cycle detection, topological sort")

        # Topological sort is only for directed graphs
        if not self.directed:
            print("Graph is not directed; topological sort is only defined for directed acyclic graphs.")
            return []

        self.color = {v: "white" for v in self.vertices}
        self.post_order = []
        self.pre_order = []
        has_cycle = False

        def dfs_visit(u):
            nonlocal has_cycle
            self.color[u] = "gray"
            for v in self.adj[u]:
                if self.color[v] == "white":
                    dfs_visit(v)
                    if has_cycle:
                        return
                elif self.color[v] == "gray":
                    # back edge -> cycle
                    has_cycle = True
                    return
            self.color[u] = "black"
            self.post_order.append(u)

        # Run DFS over all vertices (in case graph is not fully connected)
        for v in self.vertices:
            if self.color[v] == "white":
                dfs_visit(v)
                if has_cycle:
                    break

        if has_cycle:
            print("Graph has a cycle; no topological ordering exists.")
            return []

        topo_order = list(reversed(self.post_order))
        print("Topological order:", topo_order)
        return topo_order


# Example usage
if __name__ == "__main__":
    g = Graph(directed=False)
    g.add_edge("A", "B")
    g.add_edge("A", "C")
    g.add_edge("B", "C")
    g.add_edge("C", "D")

    g.print()

    
    g1 = Graph (directed=False)
    g1.initialize_from_file("dressing.txt")
    g1.print()

    g2 = Graph (directed=False)
    g2.initialize_from_file("undirected_graph.txt")
    g2.print()

    # Todo #1 Test BFS on g2 using node B as source node 
    # print out the d[], and pred[] dict after BFS() 
    g2.BFS("B")
    print("d:", g2.d)
    print("pred:", g2.pred)

    # Todo #2: Find shortest hop path in g1 from one node to another 
    print(g1.ShortestHopPath("undershorts", "jacket"))

    # Todo #3: test DFS_Graph on g1, print the pre-order and post-order 
    g1.DFS_Graph()
    print("pre-order:", g1.pre_order)
    print("post-order:", g1.post_order)

    # Todo #4: test DFS_TopoSort on g2, print the topological order 
    g2.DAG_TopoSort()

    # Todo #5: add an edge to g2 to make it cyclic, and test DFS_TopoSort on g2, 
    #  it should report there is a cycle 
    g2.add_edge("J", "B")
    g2.DAG_TopoSort()

    # Todo #6: test DFS_TopoSort 
    g2.DAG_TopoSort()




