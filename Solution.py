import sys
from Graph import graph
from Model import Route


class Solution:

    def __init__(self, model):
        self.total_profit = 0
        self.routes = [Route() for x in range(6)]
        self.matrix = model.matrix
        self.all_nodes = model.allNodes

    def update_dependent(self, route, node):
        """Updates route dependent values, total profit and node is_routed flag"""
        self.total_profit += node.profit
        route.truck.max_capacity -= node.demand
        route.truck.max_duration -= node.service_time + self.matrix[route.nodes[-1]][node.ID]
        self.all_nodes[node.ID].is_routed = True

    def print_solution(self):
        """Prints final solution"""
        print("Total Profit")
        print(self.total_profit)
        for i in range(len(self.routes)):
            print("Route " + str(i + 1))
            print(*self.routes[i].nodes)
            # debug purposes
            # print("Duration " + str(self.routes[i].truck.max_duration))
            # print("Capacity " + str(self.routes[i].truck.max_capacity))

    def solve(self):
        """VRP Solver"""
        # at least one route on the road
        print(self.matrix[269][0])
        print(self.matrix[7][320] + self.matrix[320][0])
        while not all(route.returned for route in self.routes):
            for route in self.routes:
                # route on the road
                if not route.returned:
                    min_value = sys.maxsize  # min to infinity
                    # Searching all nodes
                    for i in range(len(self.all_nodes)):
                        # find min distance if there is enough capacity and duration
                        if self.matrix[route.nodes[-1]][i] < min_value \
                                and not self.all_nodes[i].is_routed \
                                and route.truck.max_duration - self.all_nodes[i].service_time \
                                - self.matrix[route.nodes[-1]][i] - self.matrix[i][0] >= 0 \
                                and route.truck.max_capacity - self.all_nodes[i].demand >= 0:
                            min_value = self.matrix[route.nodes[-1]][i]  # min distance
                    # ValueError on .index() if route has to return to depot
                    try:
                        node_id = self.matrix[route.nodes[-1]].index(min_value)
                        node = self.all_nodes[node_id]
                        node.is_routed = True
                        self.update_dependent(route, node)
                        route.nodes.append(node_id)
                    except ValueError:
                        route.nodes.append(0)
                        route.truck.max_duration -= self.matrix[route.nodes[-1]][0]
                        route.returned = True

        self.print_solution()
        # graph(self, self.routes)
