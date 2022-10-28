import util
import sys
import pygame

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

    # creates the graph
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

    # dfs to check for connectivity
    def is_connected(self):
        visited = set()
        stack = []
        stack.append(list(self.nodes.values())[0])
        return Graph.__is_connected(self, visited, stack)

    def __is_connected(self, visited, stack):
        if not stack:
            if len(visited) == len(self.nodes): return True
            else: return False
        n = stack.pop()
        if n in visited: return Graph.__is_connected(self, visited, stack)
        visited.add(n)
        for c in n.neighbors.keys():
            stack.append(self.nodes[c])
        return Graph.__is_connected(self, visited, stack)

    # visualizes the current graph
    def visualize(self, width=1000, aspect_ratio=1, building_color=(0,0,255), node_color=(0,0,0), path_color=(0,0,0), building_radius=5, node_radius=1, path_width=1):
        pygame.init()
        display_dimensions = [aspect_ratio * width, width]
        screen = pygame.display.set_mode(display_dimensions)
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
            screen.fill((255,255,255))
            for node_coordinates in self.nodes.keys():
                c = Graph.__normalize_coordinates(node_coordinates, display_dimensions)
                pygame.draw.circle(screen, node_color, c, node_radius)
            for building in self.buildings:
                c = Graph.__normalize_coordinates(building.coordinates, display_dimensions)
                pygame.draw.circle(screen, building_color, c, building_radius)
            for path in self.paths:
                c_start = Graph.__normalize_coordinates(path.start, display_dimensions)
                c_end = Graph.__normalize_coordinates(path.end, display_dimensions)
                pygame.draw.line(screen, path_color, c_start, c_end, path_width)
            pygame.display.flip()
        pygame.quit()

    # normalizes coordinates to the pygame display
    def __normalize_coordinates(coordinates, display_dimensions, padding=10, max_x=4000, max_y=3000):
        percent_x = float(coordinates[0]) / max_x
        percent_y = float(coordinates[1]) / max_y
        new_x = percent_x * display_dimensions[0]
        new_y = percent_y * display_dimensions[0]
        return (new_x + padding, new_y + padding)

    # returns the set of paths traversed by bfs up to a certain depth
    def bfs_paths(self, start_node, depth=3):
        visited = set()
        traversed = set()
        queue = []
        queue.append(start)
        current_depth = 0
        while queue and current_depth <= depth:
            n = queue.pop(0)
            if n in visited: continue
            visited.add(n)
            for c in n.neighbors.keys():
                edge = n.neighbors[c]
                traversed.append(edge)
            current_depth += 1
        return traversed

# default limit too low for graph this size            
sys.setrecursionlimit(100000)
g = Graph()
g.construct()
"""
print('min_x = ' + str(g.parser.min_x))
print('min_y = ' + str(g.parser.min_y))
print('max_x = ' + str(g.parser.max_x))
print('max_y = ' + str(g.parser.max_y))
print('is_connected = ' + str(g.is_connected()))
"""
"""
g.visualize()
"""
# get a node from the graph
key = None
for k in g.nodes.keys():
    key = k
    break
# use key to get node
node = g.nodes[key]
paths = g.bfs_paths(node)
for p in paths:
    print(p)
