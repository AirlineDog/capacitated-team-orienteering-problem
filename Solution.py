import sys
from Graph import graph
from Model import Route, Node


class RelocationMove:
    def __init__(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = None

    def initialize(self):
        self.originRoutePosition = None
        self.targetRoutePosition = None
        self.originNodePosition = None
        self.targetNodePosition = None
        self.costChangeOriginRt = None
        self.costChangeTargetRt = None
        self.moveCost = 10 ** 9

    def store_best_relocation_move(self, originRouteIndex, targetRouteIndex, originNodeIndex, targetNodeIndex,
                                   moveCost, originRtCostChange, targetRtCostChange):
        self.originRoutePosition = originRouteIndex
        self.originNodePosition = originNodeIndex
        self.targetRoutePosition = targetRouteIndex
        self.targetNodePosition = targetNodeIndex
        self.costChangeOriginRt = originRtCostChange
        self.costChangeTargetRt = targetRtCostChange
        self.moveCost = moveCost


class Solution:

    def __init__(self, model):
        self.total_profit = 0
        self.routes = [Route() for x in range(6)]
        self.matrix = model.matrix
        self.all_nodes = model.all_nodes

    def update_dependent(self, node_id, route):
        """Updates route dependent values, total profit and node is_routed flag"""
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
        """Finds the next node to be visited"""
        min_value = sys.maxsize  # min to infinity
        node_id = -1
        for i in range(len(self.all_nodes)):
            # if there is enough capacity and duration
            if not self.all_nodes[i].is_routed \
                    and route.truck.max_duration - self.all_nodes[i].service_time \
                    - self.matrix[route.nodes[-1]][i] - self.matrix[i][0] >= 0 \
                    and route.truck.max_capacity - self.all_nodes[i].demand >= 0:
                # selection condition
                if self.matrix[route.nodes[-1]][i] / self.all_nodes[i].profit < min_value:
                    min_value = self.matrix[route.nodes[-1]][i] / self.all_nodes[i].profit
                    node_id = i
        return node_id

    def initial_solution(self):
        """VRP initial solution solver"""
        for route in self.routes:
            # route on the road
            while not route.returned:  # next route waits for the previous to return
                node_id = self.find_next_node(route)
                if node_id != -1:
                    self.update_dependent(node_id, route)
                else:
                    route.truck.max_duration -= self.matrix[route.nodes[-1]][0]
                    route.nodes.append(0)
                    route.returned = True

    def relocation_LS(self):
        """Implements VRP Relocation Local Search"""
        rm = RelocationMove()
        termination = False
        while termination is False:
            rm.initialize()
            self.find_best_relocation_move(rm)
            if rm.originRoutePosition is not None:
                if rm.moveCost < 0:
                    self.apply_relocation_move(rm)
                else:
                    termination = True

    def find_best_relocation_move(self, rm):
        """Finds best relocation move"""
        for originRouteIndex in range(0, len(self.routes)):
            rt1: Route = self.routes[originRouteIndex]
            for targetRouteIndex in range(0, len(self.routes)):
                rt2: Route = self.routes[targetRouteIndex]
                for originNodeIndex in range(1, len(rt1.nodes) - 1):
                    for targetNodeIndex in range(0, len(rt2.nodes) - 1):

                        if originRouteIndex == targetRouteIndex and (
                                targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            continue

                        # Origin nodes (B is to be changed)
                        A: Node = self.all_nodes[rt1.nodes[originNodeIndex - 1]]
                        B: Node = self.all_nodes[rt1.nodes[originNodeIndex]]
                        C: Node = self.all_nodes[rt1.nodes[originNodeIndex + 1]]
                        # Target Nodes
                        F: Node = self.all_nodes[rt2.nodes[targetNodeIndex]]
                        G: Node = self.all_nodes[rt2.nodes[targetNodeIndex + 1]]

                        # route not out of capacity
                        if rt1 != rt2:
                            if rt2.truck.max_capacity - B.demand < 0:
                                continue

                        # Distance costs
                        costAdded = self.matrix[A.ID][C.ID] + self.matrix[F.ID][B.ID] + self.matrix[B.ID][G.ID]
                        costRemoved = self.matrix[A.ID][B.ID] + self.matrix[B.ID][C.ID] + self.matrix[F.ID][G.ID]

                        moveCost = costAdded - costRemoved

                        # finds minimum moveCost
                        if moveCost < rm.moveCost:
                            # Distance + service time costs
                            originRtCostChange = self.matrix[A.ID][C.ID] \
                                                 - self.matrix[A.ID][B.ID] - self.matrix[B.ID][C.ID] - B.service_time
                            targetRtCostChange = self.matrix[F.ID][B.ID] + self.matrix[B.ID][G.ID] \
                                                 - self.matrix[F.ID][G.ID] + B.service_time
                            # route not out of time
                            if rt2.truck.max_duration - targetRtCostChange > 0:
                                rm.store_best_relocation_move(originRouteIndex, targetRouteIndex, originNodeIndex,
                                                              targetNodeIndex, moveCost, originRtCostChange,
                                                              targetRtCostChange)

    def apply_relocation_move(self, rm: RelocationMove):
        originRt: Route = self.routes[rm.originRoutePosition]
        targetRt: Route = self.routes[rm.targetRoutePosition]

        # Changing node ID
        B: int = originRt.nodes[rm.originNodePosition]

        if originRt == targetRt:
            del originRt.nodes[rm.originNodePosition]
            if rm.originNodePosition < rm.targetNodePosition:
                targetRt.nodes.insert(rm.targetNodePosition, B)
            else:
                targetRt.nodes.insert(rm.targetNodePosition + 1, B)

            originRt.truck.max_duration -= rm.moveCost
        else:
            del originRt.nodes[rm.originNodePosition]
            targetRt.nodes.insert(rm.targetNodePosition + 1, B)
            originRt.truck.max_duration -= rm.costChangeOriginRt
            targetRt.truck.max_duration -= rm.costChangeTargetRt
            originRt.truck.max_capacity += self.all_nodes[B].demand
            targetRt.truck.max_capacity -= self.all_nodes[B].demand

    def solve(self):
        """VRP Complete Solver"""
        self.initial_solution()
        self.relocation_LS()
        self.print_solution()
        graph(self, self.routes)
