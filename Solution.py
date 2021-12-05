from Model import *
from Graph import *


class Solution:

    def __init__(self, model):
        self.total_profit = 0
        self.routes = [Route() for x in range(6)]
        self.matrix = model.matrix
        self.all_nodes = model.allNodes

    def update_dependent(self, route, node):
        self.total_profit += node.profit
        route.truck.max_capacity -= node.demand
        route.truck.max_duration -= node.service_time + self.matrix[route.nodes[-1]][node.ID]
        self.all_nodes[node.ID].is_routed = True

    def solve(self):
        while not all(route.returned for route in self.routes):
            for route in self.routes:
                if not route.returned:
                    min_value = sys.maxsize
                    for i in range(len(self.all_nodes)):
                        if self.matrix[route.nodes[-1]][i] < min_value \
                                and not self.all_nodes[i].is_routed \
                                and route.truck.max_duration - self.all_nodes[i].service_time \
                                - self.matrix[route.nodes[-1]][i] - self.matrix[i][0] >= 0 \
                                and route.truck.max_capacity - self.all_nodes[i].demand >= 0:
                            min_value = self.matrix[route.nodes[-1]][i]
                    try:
                        node_id = self.matrix[route.nodes[-1]].index(min_value)
                        node = self.all_nodes[node_id]
                        node.is_routed = True
                        route.nodes.append(node_id)
                        self.update_dependent(route, node)
                    except ValueError:
                        route.nodes.append(0)
                        route.truck.max_duration -= self.matrix[route.nodes[-1]][0]
                        route.returned = True

        print(self.total_profit)

        graph(self, self.routes)
