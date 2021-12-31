import time

from Graph import graph
from Model import *
from Solution import *

start = time.time()
rand.seed(10)
mod = Model()
mod.load_model("Instance.txt")
mod.build_matrices()
s = Solution(mod)
n = 570
test_sol = Solution(mod)
test_sol.initialize(mod)
pos = 0
for i in range(n):
    test_sol.initialize(mod)
    test_sol.solve()
    if test_sol.total_profit > s.total_profit:
        s.total_profit = test_sol.total_profit
        s.routes = test_sol.routes
        pos = i
    if test_sol.total_profit > 1040:
        print(test_sol.total_profit, i)
print("finish")
print(s.total_profit, pos)
s.print_solution()
end = time.time()
print(end-start)
graph(s, s.routes)
