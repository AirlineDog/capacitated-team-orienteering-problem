import math


class Model:
    def __init__(self):
        self.all_nodes = []
        self.matrix = []
        self.vehicles = 0
        self.capacity = 0
        self.time_limit = 0
        self.new_matrix = []

    def build_new_matrix(self):
        """builds cost matrix"""
        rows = len(self.all_nodes)
        self.new_matrix = [[0.0 for x in range(rows)] for y in range(rows)]

        for i in range(0, rows):
            for j in range(1, len(self.all_nodes)):
                a = self.all_nodes[i]
                b = self.all_nodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                mat = (dist + self.all_nodes[j].service_time + self.all_nodes[j].demand) / self.all_nodes[j].profit
                self.new_matrix[i][j] = mat

    def build_cost_matrix(self):
        """builds cost matrix"""
        rows = len(self.all_nodes)
        self.matrix = [[0.0 for x in range(rows)] for y in range(rows)]

        for i in range(0, rows):
            for j in range(0, len(self.all_nodes)):
                a = self.all_nodes[i]
                b = self.all_nodes[j]
                dist = math.sqrt(math.pow(a.x - b.x, 2) + math.pow(a.y - b.y, 2))
                self.matrix[i][j] = dist

    def load_model(self, file_name):
        all_lines = list(open(file_name, "r"))

        line_counter = 0
        ln = all_lines[line_counter]
        no_spaces = ln.split(sep='\t')
        self.vehicles = int(no_spaces[1])

        line_counter += 1
        ln = all_lines[line_counter]
        no_spaces = ln.split(sep='\t')
        self.capacity = int(no_spaces[1])

        line_counter += 1
        ln = all_lines[line_counter]
        no_spaces = ln.split(sep='\t')
        self.time_limit = int(no_spaces[1])

        line_counter += 3
        ln = all_lines[line_counter]

        no_spaces = ln.split(sep='\t')
        x = float(no_spaces[1])
        y = float(no_spaces[2])
        depot = Node(0, x, y)
        depot.is_routed = True
        self.all_nodes.append(depot)

        line_counter += 2
        ln = all_lines[line_counter]
        no_spaces = ln.split(sep='\t')
        tot_customers = int(no_spaces[1])

        line_counter += 4

        for i in range(tot_customers):
            ln = all_lines[line_counter]
            no_spaces = ln.split(sep='\t')
            idd = int(no_spaces[0])
            x = float(no_spaces[1])
            y = float(no_spaces[2])
            demand = int(no_spaces[3])
            st = int(no_spaces[4])
            profit = int(no_spaces[5])
            customer = Node(idd, x, y, demand, st, profit)
            self.all_nodes.append(customer)
            line_counter += 1


class Node:
    def __init__(self, idd, xx, yy, dem=0, st=0, prf=0):
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
