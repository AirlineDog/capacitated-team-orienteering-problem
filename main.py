import time

from Graph import graph
from Model import *
from Solution import *

start = time.time()
rand.seed(20)
mod = Model()
mod.load_model("Instance.txt")
mod.build_matrices()
s = Solution(mod)
n = 1310
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
s.print_solution()
end = time.time()
print(str((end-start)//60) + " Minutes, " + str((end-start)%60) + " Seconds")
graph(s, s.routes)
