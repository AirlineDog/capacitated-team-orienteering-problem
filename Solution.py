from Model import *


class Solution:

    def __init__(self, m):
        self.total_profit = 0
        self.routes = []
        self.matrix = m.matrix
        self.all_nodes = m.allNodes

    def solve(self):
        next = min(self.matrix[0])
        x = self.matrix[0].index(next)
        f = self.all_nodes[x]
        next = min(self.matrix[x])
        x = self.matrix[x].index(next)
        f = self.all_nodes[x]
        next = min(self.matrix[x])
        x = self.matrix[x].index(next)
        f = self.all_nodes[x]
        print()
