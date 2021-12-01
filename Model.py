import math
import sys


class Model:
    def __init__(self):
        self.allNodes = []
        self.matrix = []
        self.max_capacity = 150
        self.vehicles = 6
        self.max_duration = 200

    def build_model(self):
        with open("Instance.csv") as file:
            lines = file.readlines()
        depot = Node(0, 23.142, 11.736, 0, 0, 0)
        self.allNodes.append(depot)
        total_customers = 336
        for i in range(0, total_customers):
            data = lines[11 + i].strip().split(",")
            id = int(data[0])
            x = float(data[1])
            y = float(data[2])
            dem = int(data[3])
            st = int(data[4])
            prf = int(data[5])
            self.allNodes.append(Node(id, x, y, dem, st, prf))

        rows = len(self.allNodes)
        self.matrix = [[0.0 for x in range(rows)] for y in range(rows)]

        for i in range(0, rows):
            for j in range(0, len(self.allNodes)):
                a = self.allNodes[i]
                b = self.allNodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                if dist > 0:
                    self.matrix[i][j] = dist
                else:
                    self.matrix[i][j] = sys.maxsize


class Node:
    def __init__(self, idd, xx, yy, dem, st, prf):
        self.x = xx
        self.y = yy
        self.id = idd
        self.demand = dem
        self.service_time = st
        self.profit = prf
        self.isRouted = False


class Routes:
    def __init__(self):
        self.nodes = []
