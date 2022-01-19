import random as rand
from Model import Route, Node


class TwoOptMove(object):
    """Class for storing 2opt moves"""

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
        self.moveCost = 0

    def store_best_two_opt_move(self, rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost):
        self.positionOfFirstRoute = rtInd1
        self.positionOfSecondRoute = rtInd2
        self.positionOfFirstNode = nodeInd1
        self.positionOfSecondNode = nodeInd2
        self.moveCost = moveCost


class RelocationMove:
    """Class for storing Relocation moves"""

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
        self.moveCost = 0

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
    """Class for storing addition moves"""

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


class DestroyRepair:
    """Class for storing Destroy & Repair moves"""

    def __init__(self):
        self.route = None
        self.rm_node = None
        self.add_node = None
        self.cost = None
        self.new_demand = None
        self.new_profit = None
        self.in_place = None
        self.out_place = None

    def initialize(self):
        self.route = None
        self.rm_node = None
        self.add_node = None
        self.cost = None
        self.new_demand = None
        self.new_profit = 0
        self.in_place = None
        self.out_place = None

    def store_best_destroy_repair(self, route, rm_node, add_node, cost, new_demand, new_profit, in_place, out_place):
        self.route = route
        self.rm_node = rm_node
        self.add_node = add_node
        self.cost = cost
        self.new_demand = new_demand
        self.new_profit = new_profit
        self.in_place = in_place
        self.out_place = out_place


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

    def initialize(self, model):
        self.total_profit = 0
        self.vehicles = model.vehicles
        self.capacity = model.capacity
        self.time_limit = model.time_limit
        self.routes = [Route(self.capacity, self.time_limit) for x in range(self.vehicles)]
        self.matrix = model.matrix
        self.all_nodes = model.all_nodes
        self.selection_matrix = model.selection_matrix
        for node in self.all_nodes[1:]:
            node.is_routed = False

    def print_solution(self):
        """Prints sol.txt file with the final solution"""
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

    def initial_solution(self):
        """Finds an initial solution for the VRP"""
        for route in self.routes:
            # route on the road
            while not route.returned:  # next route waits for the previous to return
                node_id = self.find_next_node_rand(route)  # best node to visit next
                if node_id is not None:
                    self.update_dependent(node_id, route)
                else:
                    # route has to return to depot
                    route.truck.duration_left -= self.matrix[route.nodes[-1]][0]
                    route.nodes.append(0)
                    route.returned = True

    def find_next_node_rand(self, route):
        """Finds the next node to be visited"""
        min_li = [(value, i) for i, value in enumerate(self.selection_matrix[route.nodes[-1]][1:], start=1)]
        min_li = sorted(min_li)  # best nodes in the beginning
        best_li = []
        # select a number of the best nodes
        for i in range(len(min_li)):
            if len(best_li) < 7:
                if not self.all_nodes[min_li[i][1]].is_routed \
                        and route.truck.duration_left - self.all_nodes[min_li[i][1]].service_time \
                        - self.matrix[route.nodes[-1]][min_li[i][1]] - self.matrix[min_li[i][1]][0] >= 0 \
                        and route.truck.capacity_left - self.all_nodes[min_li[i][1]].demand >= 0:
                    best_li.append(min_li[i][1])
            else:
                break
        # randomly select one of the best nodes
        population = [0, 1, 2, 3, 4, 5, 6]
        weights = [7, 6, 5, 4, 3, 2, 1]
        if best_li:
            rand_index = rand.choices(population[:len(best_li)], weights[:len(best_li)])
            return best_li[rand_index[0]]
        else:
            return None

    def update_dependent(self, node_id, route):
        """Updates route dependent values, total profit and node is_routed flag"""
        node = self.all_nodes[node_id]
        node.is_routed = True
        self.total_profit += node.profit
        route.profit += node.profit
        route.truck.capacity_left -= node.demand
        route.truck.duration_left -= node.service_time + self.matrix[route.nodes[-1]][node.ID]
        route.nodes.append(node_id)

    def relocation_LS(self):
        """Implements VRP Relocation Local Search"""
        rm = RelocationMove()
        termination = False
        while termination is False:
            rm.initialize()
            self.find_best_relocation_move(rm)
            # Move lowers the moving cost
            if rm.moveCost < -0.01:
                self.apply_relocation_move(rm)
            # no improving found
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
                        if self.matrix[rt1.nodes[originNodeIndex]][rt2.nodes[targetNodeIndex]] > 50:
                            # The two nodes are far from each other
                            continue
                        if originRouteIndex == targetRouteIndex \
                                and (targetNodeIndex == originNodeIndex or targetNodeIndex == originNodeIndex - 1):
                            # Same route same nodes
                            continue

                        # Origin route nodes (B is to be changed)
                        A: Node = self.all_nodes[rt1.nodes[originNodeIndex - 1]]
                        B: Node = self.all_nodes[rt1.nodes[originNodeIndex]]
                        C: Node = self.all_nodes[rt1.nodes[originNodeIndex + 1]]

                        if rt1 != rt2:
                            if rt2.truck.capacity_left - B.demand < 0:
                                # route out of capacity
                                continue

                        # Target route Nodes
                        F: Node = self.all_nodes[rt2.nodes[targetNodeIndex]]
                        G: Node = self.all_nodes[rt2.nodes[targetNodeIndex + 1]]

                        # Distance costs
                        costAdded = self.matrix[A.ID][C.ID] + self.matrix[F.ID][B.ID] + self.matrix[B.ID][G.ID]
                        costRemoved = self.matrix[A.ID][B.ID] + self.matrix[B.ID][C.ID] + self.matrix[F.ID][G.ID]

                        moveCost = costAdded - costRemoved

                        # finds minimum moveCost
                        if moveCost < rm.moveCost:
                            # Distance + service time costs
                            originRtCostChange = self.matrix[A.ID][C.ID] - self.matrix[A.ID][B.ID] \
                                                 - self.matrix[B.ID][C.ID] - B.service_time
                            targetRtCostChange = self.matrix[F.ID][B.ID] + self.matrix[B.ID][G.ID] \
                                                 - self.matrix[F.ID][G.ID] + B.service_time

                            if rt2.truck.duration_left - targetRtCostChange > 0:
                                # route is not out of time
                                rm.store_best_relocation_move(originRouteIndex, targetRouteIndex, originNodeIndex,
                                                              targetNodeIndex, moveCost, originRtCostChange,
                                                              targetRtCostChange)

    def apply_relocation_move(self, rm: RelocationMove):
        """Applies the relocation move"""
        originRt: Route = self.routes[rm.originRoutePosition]
        targetRt: Route = self.routes[rm.targetRoutePosition]

        # Changing node ID
        B: int = originRt.nodes[rm.originNodePosition]

        if originRt == targetRt:
            # A--->B--->C--->F--->G  >  A--->C--->F--->B--->G
            #      V           ^
            #      |           |
            #      \-----------/
            del originRt.nodes[rm.originNodePosition]
            if rm.originNodePosition < rm.targetNodePosition:
                targetRt.nodes.insert(rm.targetNodePosition, B)
            else:
                targetRt.nodes.insert(rm.targetNodePosition + 1, B)

            originRt.truck.duration_left -= rm.moveCost
        else:
            # A--->B--->C   >   A--->C
            #      |        >
            #      V        >
            #    F--->G     > F--->B--->G
            del originRt.nodes[rm.originNodePosition]
            targetRt.nodes.insert(rm.targetNodePosition + 1, B)
            originRt.truck.duration_left -= rm.costChangeOriginRt
            targetRt.truck.duration_left -= rm.costChangeTargetRt
            originRt.truck.capacity_left += self.all_nodes[B].demand
            targetRt.truck.capacity_left -= self.all_nodes[B].demand

    def two_opt_LS(self):
        """Implements VRP Relocation Local Search"""
        top = TwoOptMove()
        terminationCondition = False
        while terminationCondition is False:
            top.initialize()
            self.find_best_two_opt_move(top)
            # initialize route segment loads and durations
            for route in self.routes:
                route.segment_load = [0]
                route.segment_duration = [0]
            # Move lowers the cost
            if top.moveCost < -0.01:
                self.apply_two_opt_move(top)
            # no improving move found
            else:
                terminationCondition = True

    def find_best_two_opt_move(self, top):
        """Finds best 2opt move"""
        # calculate route load and duration until node inclusive
        for route in self.routes:
            for i in range(1, len(route.nodes)):
                node_id = route.nodes[i]
                route.segment_duration.append(route.segment_duration[-1] + self.matrix[route.nodes[i - 1]][node_id]
                                              + self.all_nodes[node_id].service_time)
                route.segment_load.append(route.segment_load[-1] + self.all_nodes[node_id].demand)

        for rtInd1 in range(0, len(self.routes)):
            rt1: Route = self.routes[rtInd1]
            for rtInd2 in range(rtInd1, len(self.routes)):
                rt2: Route = self.routes[rtInd2]
                for nodeInd1 in range(0, len(rt1.nodes) - 1):
                    start2 = 0
                    if rt1 == rt2:
                        start2 = nodeInd1 + 2

                    for nodeInd2 in range(start2, len(rt2.nodes) - 1):
                        if self.matrix[rt1.nodes[nodeInd1]][rt2.nodes[nodeInd2]] > 40:
                            # The two nodes are far from each other

                            continue

                        # Origin route nodes
                        A = self.all_nodes[rt1.nodes[nodeInd1]]
                        B = self.all_nodes[rt1.nodes[nodeInd1 + 1]]

                        # Target route nodes
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
                            if self.duration_is_violated(rt1, nodeInd1, rt2, nodeInd2):
                                continue
                            costAdded = self.matrix[A.ID][L.ID] + self.matrix[B.ID][K.ID]
                            costRemoved = self.matrix[A.ID][B.ID] + self.matrix[K.ID][L.ID]
                            moveCost = costAdded - costRemoved
                        if moveCost < top.moveCost:
                            top.store_best_two_opt_move(rtInd1, rtInd2, nodeInd1, nodeInd2, moveCost)

    def capacity_is_violated(self, rt1, nodeInd1, rt2, nodeInd2):
        """Checks if capacity is violated"""
        rt1FirstSegmentLoad = rt1.segment_load[nodeInd1]
        rt1SecondSegmentLoad = (rt1.max_capacity - rt1.truck.capacity_left) - rt1FirstSegmentLoad

        rt2FirstSegmentLoad = rt2.segment_load[nodeInd2]
        rt2SecondSegmentLoad = (rt2.max_capacity - rt2.truck.capacity_left) - rt2FirstSegmentLoad
        if rt1FirstSegmentLoad + rt2SecondSegmentLoad > rt1.max_capacity:
            return True
        if rt2FirstSegmentLoad + rt1SecondSegmentLoad > rt2.max_capacity:
            return True

        return False

    def duration_is_violated(self, rt1, nodeInd1, rt2, nodeInd2):
        """Checks if duration is violated"""
        rt1FirstSegmentDuration = rt1.segment_duration[nodeInd1]
        rt1SecondSegmentDuration = rt1.max_duration - rt1.truck.duration_left - rt1FirstSegmentDuration

        rt2FirstSegmentDuration = rt2.segment_duration[nodeInd2]
        rt2SecondSegmentDuration = rt2.max_duration - rt2.truck.duration_left - rt2FirstSegmentDuration

        # Second segments include the duration from the route breakpoint AB add KL
        # Must be removed
        rt1SecondSegmentDuration -= self.matrix[rt1.nodes[nodeInd1]][rt1.nodes[nodeInd1 + 1]]
        rt2SecondSegmentDuration -= self.matrix[rt2.nodes[nodeInd2]][rt2.nodes[nodeInd2 + 1]]

        AL = self.matrix[rt1.nodes[nodeInd1]][rt2.nodes[nodeInd2 + 1]]
        KB = self.matrix[rt2.nodes[nodeInd2]][rt1.nodes[nodeInd1 + 1]]

        # The new arcs should be added
        if rt1FirstSegmentDuration + rt2SecondSegmentDuration + AL > rt1.max_duration:
            return True
        if rt2FirstSegmentDuration + rt1SecondSegmentDuration + KB > rt2.max_duration:
            return True

        return False

    def apply_two_opt_move(self, top):
        """Applies the 2opt move"""
        rt1: Route = self.routes[top.positionOfFirstRoute]
        rt2: Route = self.routes[top.positionOfSecondRoute]

        if rt1 == rt2:
            # A-->B-->C-->K-->L-->M
            #
            #
            # /-----------\
            # |           |
            # |           V
            # A   B<--C<--K   L-->M
            #     |           ^
            #     |           |
            #     \-----------/
            #
            #
            # A-->K-->C-->B-->L-->M

            # reverses the nodes in the segment [positionOfFirstNode + 1,  top.positionOfSecondNode]
            reversedSegment = reversed(rt1.nodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1])
            rt1.nodes[top.positionOfFirstNode + 1: top.positionOfSecondNode + 1] = reversedSegment
            rt1.truck.duration_left -= top.moveCost

        else:
            # A-->B
            #
            # K-->L
            #
            # A-\ /->B
            #    X
            # K-/ \->L
            #
            # A-->L
            #
            # K-->B

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
        """Updates duration and capacity"""
        truck_capacity_used = 0
        truck_duration_used = 0
        for i in range(0, len(rt.nodes) - 1):
            A = self.all_nodes[rt.nodes[i]]
            B = self.all_nodes[rt.nodes[i + 1]]
            truck_capacity_used += self.matrix[A.ID][B.ID] + A.service_time
            truck_duration_used += A.demand
        rt.truck.capacity_left = rt.max_capacity - truck_duration_used
        rt.truck.duration_left = rt.max_duration - truck_capacity_used

    def add_nodes(self):
        """Adds nodes to the solution after Local Search cost reduction"""
        am = AdditionMove()
        for route in self.routes:
            flag = False  # more additions to be done
            while not flag:
                am.initialize()
                max_overall = -1
                for place in range(len(route.nodes) - 1):
                    max_prof = -2
                    position = 0
                    move_cost = 0
                    for i in range(len(self.all_nodes)):
                        # nodes close to each other
                        if self.matrix[route.nodes[place]][i] < 50:
                            node = self.all_nodes[i]
                            if not node.is_routed:
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
        """Applies the addition move"""
        #   C       >
        #   |       >
        #   V       >
        # A--->B    >  A-->C-->B

        am.additionRoute.nodes.insert(am.additionPosition + 1, am.addingNode.ID)
        am.additionRoute.truck.duration_left -= am.moveCost
        am.additionRoute.truck.capacity_left -= am.addingNode.demand
        am.additionRoute.profit += am.addingNode.profit
        self.total_profit += am.addingNode.profit
        am.addingNode.is_routed = True

    def destroy_and_repair(self):
        """Destroys one node to add an other one"""
        dr = DestroyRepair()
        for route in self.routes:
            for i in range(1, len(route.nodes) - 1):
                rm_node: int = route.nodes[i]
                dr.initialize()
                for j in range(len(self.all_nodes)):
                    node: Node = self.all_nodes[j]
                    add_node = j
                    new_profit = node.profit - self.all_nodes[rm_node].profit
                    new_demand = self.all_nodes[add_node].demand - self.all_nodes[rm_node].demand
                    if node.is_routed or self.matrix[rm_node][add_node] > 50 or new_profit < dr.new_profit \
                            or route.truck.capacity_left < new_demand:
                        continue
                    for place in range(len(route.nodes) - 1):
                        if place == i or place == i - 1:
                            rm_cost = self.matrix[route.nodes[i - 1]][rm_node] \
                                      + self.matrix[rm_node][route.nodes[i + 1]] \
                                      + self.all_nodes[rm_node].service_time
                            add_cost = self.matrix[route.nodes[i - 1]][add_node] \
                                       + self.matrix[add_node][route.nodes[i + 1]] \
                                       + self.all_nodes[add_node].service_time
                        else:
                            rm_cost = self.matrix[route.nodes[i - 1]][rm_node] \
                                      + self.matrix[rm_node][route.nodes[i + 1]] \
                                      + self.all_nodes[rm_node].service_time \
                                      + self.matrix[route.nodes[place]][route.nodes[place + 1]]
                            add_cost = self.matrix[route.nodes[i - 1]][route.nodes[i + 1]] \
                                       + self.matrix[route.nodes[place]][add_node] \
                                       + self.matrix[add_node][route.nodes[place + 1]] \
                                       + self.all_nodes[add_node].service_time
                        cost = add_cost - rm_cost
                        if route.truck.duration_left > cost:
                            dr.store_best_destroy_repair(route, rm_node, add_node,
                                                         cost, new_demand, new_profit, place, i)
                if dr.route is not None:
                    self.apply_destroy_repair(dr)

    def apply_destroy_repair(self, dr):
        """Applies the destroy & repair step"""
        #             >   D     >
        #             >   |     >
        #             >   V     >
        # A--->B--->C > A--->C  >  A-->D-->C

        del dr.route.nodes[dr.out_place]
        if dr.out_place <= dr.in_place:
            dr.route.nodes.insert(dr.in_place, dr.add_node)
        else:
            dr.route.nodes.insert(dr.in_place + 1, dr.add_node)
        self.all_nodes[dr.rm_node].is_routed = False
        self.all_nodes[dr.add_node].is_routed = True
        dr.route.profit += dr.new_profit
        self.total_profit += dr.new_profit
        dr.route.truck.duration_left -= dr.cost
        dr.route.truck.capacity_left -= dr.new_demand

    def solve(self):
        """VRP Complete Solver"""
        self.initial_solution()
        improvement = True
        prof = self.total_profit
        while improvement:
            self.relocation_LS()
            self.two_opt_LS()
            self.add_nodes()
            self.destroy_and_repair()
            if prof == self.total_profit:
                improvement = False
            else:
                prof = self.total_profit
