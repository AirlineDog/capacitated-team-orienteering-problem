import matplotlib.pyplot as plt
import numpy as np


def graph(solution, routes):
    plt.figure(figsize=(8, 6), dpi=80)
    xs = [x.x for x in solution.all_nodes]
    ys = [y.y for y in solution.all_nodes]
    ids = [x.ID for x in solution.all_nodes]
    plt.scatter(xs, ys, c="blue", marker=".")
    plt.scatter(23.142, 11.736, c="black")
    plt.scatter(0, 0, c="black")
    for route in routes:
        node_xs = [solution.all_nodes[ID].x for ID in route.nodes]
        node_ys = [solution.all_nodes[ID].y for ID in route.nodes]
        plt.plot(node_xs, node_ys)
    for x, y, ID in zip(xs, ys, ids):
        plt.annotate(str(ID), xy=(x, y))
    plt.gcf().set_size_inches((30, 30))
    leg = ["Route " + str(i) + "d:" + str(solution.routes[i].truck.max_duration)
           + "c:" + str(solution.routes[i].truck.max_capacity)
           for i in range(len(solution.routes))] + [solution.total_profit]
    plt.legend(leg, loc='lower right')
    plt.savefig("test.png")
