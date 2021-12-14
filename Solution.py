import sys
from Graph import graph
from Model import Route


class Solution:

    def __init__(self, model):
        self.total_profit = 0
        self.routes = [Route() for x in range(6)]
        self.matrix = model.matrix
        self.all_nodes = model.all_nodes

    def update_dependent(self, min_value, route):
        """Updates route dependent values, total profit and node is_routed flag"""
        node_id = self.matrix[route.nodes[-1]].index(min_value)
        node = self.all_nodes[node_id]
        node.is_routed = True
        self.total_profit += node.profit
        route.truck.max_capacity -= node.demand
        route.truck.max_duration -= node.service_time + self.matrix[route.nodes[-1]][node.ID]
        self.all_nodes[node.ID].is_routed = True
        route.nodes.append(node_id)

    def print_solution(self):
        """Prints final solution"""
        with open("sol.txt", "w") as f:
            f.write("Total Profit\n")
            f.write(str(self.total_profit) + "\n")
            for i in range(len(self.routes)):
                f.write("Route " + str(i + 1) + "\n")
                nodes = ""
                for x in range(len(self.routes[i].nodes)):
                    nodes += str(self.routes[i].nodes[x]) + " "
                nodes = nodes.strip()
                f.write(nodes)
                f.write("\n")
                # debug purposes
                # print("Duration left :" + str(self.routes[i].truck.max_duration))
                # print("Capacity left :" + str(self.routes[i].truck.max_capacity))

    def find_next_node(self, route):
        min_value = sys.maxsize  # min to infinity
        # Searching all nodes
        for i in range(len(self.all_nodes)):
            # if there is enough capacity and duration
            if not self.all_nodes[i].is_routed \
                    and route.truck.max_duration - self.all_nodes[i].service_time \
                    - self.matrix[route.nodes[-1]][i] - self.matrix[i][0] >= 0 \
                    and route.truck.max_capacity - self.all_nodes[i].demand >= 0:
                if self.matrix[route.nodes[-1]][i] < min_value:
                    min_value = self.matrix[route.nodes[-1]][i]
        return min_value

    def initial_solution(self):
        """VRP Nearest neighbor Solver"""
        for route in self.routes:
            # route on the road
            for times in range(1):
                if not route.returned:
                    min_value = self.find_next_node(route)
                    # ValueError on .index() if route has to return to depot
                    try:
                        self.update_dependent(min_value, route)
                    except ValueError:
                        route.truck.max_duration -= self.matrix[route.nodes[-1]][0]
                        route.nodes.append(0)
                        route.returned = True

        for route in self.routes:
            # route on the road
            while not route.returned:  # next route waits for the previous to return
                min_value = self.find_next_node(route)
                # ValueError on .index() if route has to return to depot
                try:
                    self.update_dependent(min_value, route)
                except ValueError:
                    route.truck.max_duration -= self.matrix[route.nodes[-1]][0]
                    route.nodes.append(0)
                    route.returned = True

    def solve(self):
        """VRP Complete Solver"""
        self.initial_solution()

        self.print_solution()
        graph(self, self.routes)
