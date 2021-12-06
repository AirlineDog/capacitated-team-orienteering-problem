import math


class Model:
    def __init__(self):
        self.allNodes = []
        self.matrix = []

    def build_model(self):
        with open("Instance.csv") as file:
            lines = file.readlines()
        # initialise depot
        depot = Node(0, 23.142, 11.736, 0, 0, 0)
        depot.is_routed = True
        self.allNodes.append(depot)
        # read data form csv
        total_customers = 336
        for i in range(0, total_customers):
            data = lines[11 + i].strip().split(",")
            point_id = int(data[0])
            x = float(data[1])
            y = float(data[2])
            dem = int(data[3])
            st = int(data[4])
            prf = int(data[5])
            self.allNodes.append(Node(point_id, x, y, dem, st, prf))

        # built cost matrix
        rows = len(self.allNodes)
        self.matrix = [[0.0 for x in range(rows)] for y in range(rows)]

        for i in range(0, rows):
            for j in range(0, len(self.allNodes)):
                a = self.allNodes[i]
                b = self.allNodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                self.matrix[i][j] = dist


class Node:
    def __init__(self, idd, xx, yy, dem, st, prf):
        self.x = xx
        self.y = yy
        self.ID = idd
        self.demand = dem
        self.service_time = st
        self.profit = prf
        self.is_routed = False


class Route:
    def __init__(self):
        self.truck = Truck()
        self.nodes = [0]
        self.returned = False


class Truck:
    def __init__(self):
        self.max_capacity = 150
        self.max_duration = 200
