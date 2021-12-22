import random as rand
from copy import deepcopy

from Graph import graph
from Model import Route, Node


class TwoOptMove(object):
    def __init__(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = None

    def initialize(self):
        self.positionOfFirstRoute = None
        self.positionOfSecondRoute = None
        self.positionOfFirstNode = None
        self.positionOfSecondNode = None
        self.moveCost = 10 ** 9

    def store_best_two_opt_move(self, rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost):
        self.positionOfFirstRoute = rtInd1
        self.positionOfSecondRoute = rtInd2
        self.positionOfFirstNode = nodeInd1
        self.positionOfSecondNode = nodeInd2
        self.moveCost = moveCost


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


class AdditionMove:
    def __init__(self):
        self.additionRoute = None
        self.addingNode = None
        self.additionPosition = None
        self.moveCost = None
        self.profitGain = None

    def initialize(self):
        self.additionRoute = None
        self.addingNode = None
        self.additionPosition = None
        self.profitGain = None
        self.moveCost = None

    def store_best_addition_move(self, additionRoute, addingNode,
                                 additionPosition, moveCost):
        self.additionRoute = additionRoute
        self.addingNode = addingNode
        self.additionPosition = additionPosition
        self.profitGain = addingNode.profit
        self.moveCost = moveCost


class Solution:

    def __init__(self, model):
        self.total_profit = 0
        self.vehicles = model.vehicles
        self.capacity = model.capacity
        self.time_limit = model.time_limit
        self.routes = [Route(self.capacity, self.time_limit) for x in range(self.vehicles)]
        self.matrix = model.matrix
        self.all_nodes = model.all_nodes
        self.selection_matrix = model.selection_matrix

    def update_dependent(self, node_id, route):
        """Updates route dependent values, total profit and node is_routed flag"""
        node = self.all_nodes[node_id]
        node.is_routed = True
        self.total_profit += node.profit
        route.profit += node.profit
        route.truck.capacity_left -= node.demand
        route.truck.duration_left -= node.service_time + self.matrix[route.nodes[-1]][node.ID]
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

    def initial_solution(self):
        for route in self.routes:
            # route on the road
            while not route.returned:  # next route waits for the previous to return
                node_id = self.find_next_node(route)
                if node_id is not None:
                    self.update_dependent(node_id, route)
                else:
                    route.truck.duration_left -= self.matrix[route.nodes[-1]][0]
                    route.nodes.append(0)
                    route.returned = True

    def find_next_node(self, route):
        """Finds the next node to be visited"""
        min_li = [(value, i) for i, value in enumerate(self.selection_matrix[route.nodes[-1]][1:], start=1)]
        min_li = sorted(min_li)
        for i in range(len(min_li)):
            if not self.all_nodes[min_li[i][1]].is_routed \
                    and route.truck.duration_left - self.all_nodes[min_li[i][1]].service_time \
                    - self.matrix[route.nodes[-1]][min_li[i][1]] - self.matrix[min_li[i][1]][0] >= 0 \
                    and route.truck.capacity_left - self.all_nodes[min_li[i][1]].demand >= 0:
                return min_li[i][1]

    def initial_rand(self):
        for route in self.routes:
            # route on the road
            while not route.returned:  # next route waits for the previous to return
                node_id = self.find_next_node_rand(route)
                if node_id is not None:
                    self.update_dependent(node_id, route)
                else:
                    route.truck.duration_left -= self.matrix[route.nodes[-1]][0]
                    route.nodes.append(0)
                    route.returned = True

    def find_next_node_rand(self, route):
        """Finds the next node to be visited"""
        min_li = [(value, i) for i, value in enumerate(self.selection_matrix[route.nodes[-1]][1:], start=1)]
        min_li = sorted(min_li)
        best_li = []
        for i in range(len(min_li)):
            if len(best_li) < 3:
                if not self.all_nodes[min_li[i][1]].is_routed \
                        and route.truck.duration_left - self.all_nodes[min_li[i][1]].service_time \
                        - self.matrix[route.nodes[-1]][min_li[i][1]] - self.matrix[min_li[i][1]][0] >= 0 \
                        and route.truck.capacity_left - self.all_nodes[min_li[i][1]].demand >= 0:
                    best_li.append(min_li[i][1])
            else:
                break
        if len(best_li) == 3:
            best_index = rand.randint(0, 2)
            return best_li[best_index]
        elif len(best_li) == 2:
            best_index = rand.randint(0, 1)
            return best_li[best_index]
        elif len(best_li) == 1:
            return best_li[0]
        else:
            return None

    def relocation_LS(self):
        """Implements VRP Relocation Local Search"""
        rm = RelocationMove()
        termination = False
        while termination is False:
            rm.initialize()
            self.find_best_relocation_move(rm)
            if rm.moveCost != 10**9:
                if rm.moveCost < 0:
                    self.apply_relocation_move(rm)
                else:
                    termination = True
            else:
                termination = True

    def two_optLS(self):
        top = TwoOptMove()
        terminationCondition = False
        while terminationCondition is False:
            top.initialize()
            self.find_best_two_opt_move(top)
            if top.positionOfFirstRoute is not None:
                if top.moveCost < 0:
                    self.apply_two_opt_move(top)
                else:
                    terminationCondition = True

    def find_best_two_opt_move(self, top):
        for rtInd1 in range(0, len(self.routes)):
            rt1: Route = self.routes[rtInd1]
            for rtInd2 in range(rtInd1, len(self.routes)):
                rt2: Route = self.routes[rtInd2]
                for nodeInd1 in range(0, len(rt1.nodes) - 1):
                    start2 = 0
                    if rt1 == rt2:
                        start2 = nodeInd1 + 2

                    for nodeInd2 in range(start2, len(rt2.nodes) - 1):
                        moveCost = 10 ** 9

                        A = self.all_nodes[rt1.nodes[nodeInd1]]
                        B = self.all_nodes[rt1.nodes[nodeInd1 + 1]]
                        K = self.all_nodes[rt2.nodes[nodeInd2]]
                        L = self.all_nodes[rt2.nodes[nodeInd2 + 1]]

                        if rt1 == rt2:
                            if nodeInd1 == 0 and nodeInd2 == len(rt1.nodes) - 2:
                                continue
                            costAdded = self.matrix[A.ID][K.ID] + self.matrix[B.ID][L.ID]
                            costRemoved = self.matrix[A.ID][B.ID] + self.matrix[K.ID][L.ID]
                            moveCost = costAdded - costRemoved
                        else:
                            if nodeInd1 == 0 and nodeInd2 == 0:
                                continue
                            if nodeInd1 == len(rt1.nodes) - 2 and nodeInd2 == len(rt2.nodes) - 2:
                                continue

                            if self.capacity_is_violated(rt1, nodeInd1, rt2, nodeInd2):
                                continue
                            # if duration is violated
                        if moveCost < top.moveCost:
                            top.store_best_two_opt_move(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost)

    def capacity_is_violated(self, rt1, nodeInd1, rt2, nodeInd2):
        rt1FirstSegmentLoad = 0
        for i in range(0, nodeInd1 + 1):
            n: Node = self.all_nodes[rt1.nodes[i]]
            rt1FirstSegmentLoad += n.demand
        rt1SecondSegmentLoad = 150 - rt1FirstSegmentLoad  # fix magic number

        rt2FirstSegmentLoad = 0
        for i in range(0, nodeInd2 + 1):
            n = self.all_nodes[rt2.nodes[i]]
            rt2FirstSegmentLoad += n.demand
        rt2SecondSegmentLoad = 150 - rt2FirstSegmentLoad  # fix magic number

        if rt1FirstSegmentLoad + rt2SecondSegmentLoad > rt1.truck.capacity_left:
            return True
        if rt2FirstSegmentLoad + rt1SecondSegmentLoad > rt2.truck.capacity_left:
            return True

        return False

    def apply_two_opt_move(self, top):
        rt1: Route = self.routes[top.positionOfFirstRoute]
        rt2: Route = self.routes[top.positionOfSecondRoute]

        if rt1 == rt2:
            # reverses the nodes in the segment [positionOfFirstNode + 1,  top.positionOfSecondNode]
            reversedSegment = reversed(rt1.nodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            rt1.nodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegment
            rt1.truck.duration_left -= top.moveCost

        else:
            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt1 = rt1.nodes[top.positionOfFirstNode + 1:]

            # slice with the nodes from position top.positionOfFirstNode + 1 onwards
            relocatedSegmentOfRt2 = rt2.nodes[top.positionOfSecondNode + 1:]

            del rt1.nodes[top.positionOfFirstNode + 1:]
            del rt2.nodes[top.positionOfSecondNode + 1:]

            rt1.nodes.extend(relocatedSegmentOfRt2)
            rt2.nodes.extend(relocatedSegmentOfRt1)

            self.update_route_cost_and_load(rt1)
            self.update_route_cost_and_load(rt2)

    def update_route_cost_and_load(self, rt: Route):
        tc = 0
        tl = 0
        for i in range(0, len(rt.nodes) - 1):
            A = rt.nodes[i]
            B = rt.nodes[i + 1]
            tc += self.matrix[A.ID][B.ID]
            tl += A.demand
        rt.truck.capacity_left = rt.max_capacity - tl
        rt.truck.duration_left = rt.max_duration - tc

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
                            if rt2.truck.capacity_left - B.demand < 0:
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
                            if rt2.truck.duration_left - targetRtCostChange > 0:
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

            originRt.truck.duration_left -= rm.moveCost
        else:
            del originRt.nodes[rm.originNodePosition]
            targetRt.nodes.insert(rm.targetNodePosition + 1, B)
            originRt.truck.duration_left -= rm.costChangeOriginRt
            targetRt.truck.duration_left -= rm.costChangeTargetRt
            originRt.truck.capacity_left += self.all_nodes[B].demand
            targetRt.truck.capacity_left -= self.all_nodes[B].demand

    def add_nodes(self):
        am = AdditionMove()
        for route in self.routes:
            flag = False
            while not flag:
                am.initialize()
                max_overall = -1
                for node in self.all_nodes:
                    if not node.is_routed:
                        max_prof = -2
                        position = 0
                        move_cost = 0
                        for place in range(len(route.nodes) - 1):
                            costRemoved = self.matrix[route.nodes[place]][route.nodes[place + 1]]
                            costAdded = self.matrix[route.nodes[place]][node.ID] + self.matrix[node.ID][
                                route.nodes[place + 1]]
                            cost = costAdded - costRemoved + node.service_time
                            # enough duration and capacity
                            if cost < route.truck.duration_left \
                                    and node.demand < route.truck.capacity_left:
                                # selection condition
                                if node.profit > max_prof:
                                    max_prof = node.profit
                                    position = place
                                    move_cost = cost
                        if max_prof > max_overall:
                            max_overall = max_prof
                            am.store_best_addition_move(route, node, position, move_cost)
                if max_overall != -1:
                    self.apply_add_node(am)
                else:
                    flag = True

    def apply_add_node(self, am: AdditionMove):
        am.additionRoute.nodes.insert(am.additionPosition + 1, am.addingNode.ID)
        am.additionRoute.truck.duration_left -= am.moveCost
        am.additionRoute.truck.capacity_left -= am.addingNode.demand
        am.additionRoute.profit += am.addingNode.profit
        self.total_profit += am.addingNode.profit

    def solve(self):
        # 20 1066 88/100
        rand.seed(20)
        """VRP Complete Solver"""
        #self.initial_solution()
        n = 500
        sols = [deepcopy(self) for x in range(n)]
        for i in range(n):
            sol = sols[i]
            sol.initial_rand()
            sol.relocation_LS()
            sol.two_optLS()
            sol.add_nodes()
            if sol.total_profit > self.total_profit:
                self = sol
            print(sol.total_profit, i)
        max_sol = max(sols, key=lambda x: x.total_profit)
        print(max_sol.total_profit, sols.index(max_sol))
        self.print_solution()
        graph(self, self.routes)
