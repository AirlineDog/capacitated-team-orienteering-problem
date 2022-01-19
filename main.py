from Model import *
from Solution import *

rand.seed(20)
mod = Model()
mod.load_model("Instance.txt")
mod.build_matrices()
s = Solution(mod)
n = 1310
test_sol = Solution(mod)
for i in range(n):
    test_sol.initialize(mod)
    test_sol.solve()
    if test_sol.total_profit > s.total_profit:
        s.total_profit = test_sol.total_profit
        s.routes = test_sol.routes
s.print_solution()
