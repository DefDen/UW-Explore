import csv

class Building:
    def __init__(self, short_name, long_name, coordinate):
        self.short_name = short_name
        self.long_name = long_name
        self.coordinate = coordinate

class Path:
    def __init__(self, start, end, distance):
        self.start = start
        self.end = end
        self.distance = distance

def parse_buildings(debug=0):
    buildings = []
    with open('../data/campus_buildings.tsv') as file:
        tsv_file = csv.reader(file, delimiter='\t')
        for line in tsv_file:
            if debug:
                print(line)
            buildings.append(Building(line[0], line[1], (line[2], line[3])))
    return buildings

def parse_paths(debug=0):
    paths = []
    with open('../data/campus_paths.tsv') as file:
        tsv_file = csv.reader(file, delimiter='\t')
        for line in tsv_file:
            if debug:
                print(line)
            paths.append(Path((line[0], line[1]), (line[2], line[3]), line[4]))
    return paths
