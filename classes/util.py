import csv

class Building:
    def __init__(self, short_name, long_name, coordinates):
        self.short_name = short_name
        self.long_name = long_name
        self.coordinates = coordinates

class Path:
    def __init__(self, start, end, distance):
        self.start = start
        self.end = end
        self.distance = distance
        self.slope = Path.__find_slope(start, end)

    def __find_slope(start, end):
        return (start[1] - end[1]) / (start[0] - end[0])

class Parser:
    def __init__(self, file_path='../data'):
        self.file_path = file_path
        self.buildings = []
        self.paths = []
        self.min_x = 0
        self.min_y = 0
        self.max_x = 0
        self.max_y = 0

    def parse_buildings(self, debug=0):
        buildings = []
        with open(str(self.file_path) + '/campus_buildings.tsv') as file:
            tsv_file = csv.reader(file, delimiter='\t')
            next(tsv_file)
            for line in tsv_file:
                if debug:
                    print(line)
                buildings.append(Building(line[0], line[1], (line[2], line[3])))
                self.buildings.append(Building(line[0], line[1], (line[2], line[3])))
        return buildings

    def parse_paths(self, debug=0):
        paths = []
        with open(str(self.file_path) + '/campus_paths.tsv') as file:
            tsv_file = csv.reader(file, delimiter='\t')
            next(tsv_file)
            first = True
            for line in tsv_file:
                if first:
                    self.min_x = float(line[0])
                    self.min_y = float(line[1])
                    self.max_x = float(line[0])
                    self.max_y = float(line[1])
                    first = False
                if debug:
                    print(line)
                self.min_x = min(float(self.min_x), float(line[0]), float(line[2]))
                self.min_y = min(float(self.min_y), float(line[1]), float(line[3]))
                self.max_x = max(float(self.max_x), float(line[0]), float(line[2]))
                self.max_y = max(float(self.max_y), float(line[1]), float(line[3]))
                paths.append(Path((line[0], line[1]), (line[2], line[3]), line[4]))
                self.paths.append(Path((line[0], line[1]), (line[2], line[3]), line[4]))
        return paths
