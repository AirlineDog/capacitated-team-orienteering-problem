from Model import *
from Graph import *

class Solution:

    def __init__(self, model):
        self.total_profit = 0
        self.routes = [Route() for x in range(6)]
        self.matrix = model.matrix
        self.all_nodes = model.allNodes

    def update_dependent(self, node):
        self.total_profit += node.profit
        self.trucks[0].max_capacity -= node.demand
        self.trucks[0].max_duration -= node.service_time
        self.all_nodes[node.id].is_routed = True
        self.routes[0].nodes.append(node.id)

    def solve(self):
        # locations = [x.nodes[-1] for x in self.routes]
        # locations = list(dict.fromkeys(locations))
        # min_value = sys.maxsize
        # from_node = -1
        # for i in locations:
        #     next = min(self.matrix[i])
        #     if next < min_value:
        #         min_value = next
        #         from_node = i
        # id = self.matrix[from_node].index(min_value)
        # node = self.all_nodes[id]
        #
        # for route in self.routes:
        #     if route.nodes[-1] == from_node:
        #         route.nodes.append(id)
        #         break
        # self.update_dependent(node)
        routes = [[0], [0]]
        while len(routes[0]) + len(routes[1]) < 337:
            for route in routes:
                min_value = sys.maxsize
                for i in range(len(self.all_nodes)):
                    if self.matrix[route[-1]][i] < min_value and not self.all_nodes[i].is_routed:
                        min_value = self.matrix[route[-1]][i]
                id = self.matrix[route[-1]].index(min_value)
                node = self.all_nodes[id]
                node.is_routed = True
                route.append(id)
        routes[0].append(0)
        routes[1].append(0)
        graph(self, routes)
        print()

        # next_point = min(self.matrix[0])
        # id = self.matrix[0].index(next_point)
        # node = self.all_nodes[id]
        # self.update_dependent(node)
        # next_point = min(self.matrix[128])
