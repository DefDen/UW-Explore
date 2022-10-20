import util

class Node:
    def __init__(self, coordinates=(0,0), building=None):
        if building:
            self.coordinates = building.coordinates
        else:
            self.coordinates = coordinates
        self.building = building
        # maps destination coordinates to edge
        self.neighbors = {}

class Edge:
    def __init__(self, start=(0,0), end=(0,0), distance=0, path=None):
        if path:
            self.start = path.start
            self.end = path.end
            self.distance = path.distance
        else:
            self.start = start
            self.end = end
            self.distance = distance

class Graph:
    def __init__(self):
        self.parser = util.Parser()
        self.buildings = self.parser.parse_buildings()
        self.paths = self.parser.parse_paths()
        # maps coordinates to nodes
        self.nodes = {}

    def construct(self):
        # add edges and associated nodes to the graph
        for path in self.paths:
            # if nodes are not in graph add them
            if not path.start in self.nodes:
                self.nodes[path.start] = Node(path.start)
            if not path.end in self.nodes:
                self.nodes[path.end] = Node(path.end)
            # add edge from start of path to end of path
            self.nodes[path.start].neighbors[path.end] = Edge(path)
            # reverse the path direction and add it again (edges should not be directed)
            temp = path.start
            path.start = path.end
            path.end = temp
            self.nodes[path.start].neighbors[path.end] = Edge(path)
        # add names to the nodes where there are buildings
        for building in self.buildings:
            # if the building was not in the graph, something must have gone wrong since there would be no paths to it
            if not building.coordinates in self.nodes:
                raise Exception(str(building.short_name) + (' ') + str(building.long_name) + (' was not in the graph'))
            # update building field on node to its building
            self.nodes[building.coordinates].building = building

g = Graph()
g.construct()
print(len(g.nodes))
