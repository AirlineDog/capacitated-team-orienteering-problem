import time

from Graph import graph
from Model import *
from Solution import *
for y in range(2, 10):
    print(y)
    weights = [(71*y-17*x) for x in range(y)]
    print(weights)
    start = time.time()
    rand.seed(10)
    mod = Model()
    mod.load_model("Instance.txt")
    mod.build_cost_matrix()
    mod.build_selection_matrix()
    s = Solution(mod)
    n = 500
    test_sol = Solution(mod)
    test_sol.initialize(mod)
    pos = 0
    for i in range(n):
        test_sol.initialize(mod)
        test_sol.solve(weights)
        if test_sol.total_profit > s.total_profit:
            s.total_profit = test_sol.total_profit
            s.routes = test_sol.routes
            pos = i
        if test_sol.total_profit > 1060:
            print(test_sol.total_profit, i)
    print("finish")
    print(s.total_profit, pos)
    start = time.time()
    rand.seed(20)
    mod = Model()
    mod.load_model("Instance.txt")
    mod.build_cost_matrix()
    mod.build_selection_matrix()
    s = Solution(mod)

    test_sol = Solution(mod)
    test_sol.initialize(mod)
    pos = 0
    for i in range(n):
        test_sol.initialize(mod)
        test_sol.solve(weights)
        if test_sol.total_profit > s.total_profit:
            s.total_profit = test_sol.total_profit
            s.routes = test_sol.routes
            pos = i
        if test_sol.total_profit > 1060:
            print(test_sol.total_profit, i)
    print("finish")
    print(s.total_profit, pos)
    start = time.time()
    rand.seed(30)
    mod = Model()
    mod.load_model("Instance.txt")
    mod.build_cost_matrix()
    mod.build_selection_matrix()
    s = Solution(mod)

    test_sol = Solution(mod)
    test_sol.initialize(mod)
    pos = 0
    for i in range(n):
        test_sol.initialize(mod)
        test_sol.solve(weights)
        if test_sol.total_profit > s.total_profit:
            s.total_profit = test_sol.total_profit
            s.routes = test_sol.routes
            pos = i
        if test_sol.total_profit > 1060:
            print(test_sol.total_profit, i)
    print("finish")
    print(s.total_profit, pos)
    start = time.time()
    rand.seed(40)
    mod = Model()
    mod.load_model("Instance.txt")
    mod.build_cost_matrix()
    mod.build_selection_matrix()
    s = Solution(mod)

    test_sol = Solution(mod)
    test_sol.initialize(mod)
    pos = 0
    for i in range(n):
        test_sol.initialize(mod)
        test_sol.solve(weights)
        if test_sol.total_profit > s.total_profit:
            s.total_profit = test_sol.total_profit
            s.routes = test_sol.routes
            pos = i
        if test_sol.total_profit > 1060:
            print(test_sol.total_profit, i)
    print("finish")
    print(s.total_profit, pos)
    start = time.time()
    rand.seed(50)
    mod = Model()
    mod.load_model("Instance.txt")
    mod.build_cost_matrix()
    mod.build_selection_matrix()
    s = Solution(mod)

    test_sol = Solution(mod)
    test_sol.initialize(mod)
    pos = 0
    for i in range(n):
        test_sol.initialize(mod)
        test_sol.solve(weights)
        if test_sol.total_profit > s.total_profit:
            s.total_profit = test_sol.total_profit
            s.routes = test_sol.routes
            pos = i
        if test_sol.total_profit > 1060:
            print(test_sol.total_profit, i)
    print("finish")
    print(s.total_profit, pos)
    # s.print_solution()
    end = time.time()
    print((end-start)/60)
    # graph(s, s.routes)
