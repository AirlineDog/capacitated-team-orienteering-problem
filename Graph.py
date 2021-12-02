from Model import *
import matplotlib.pyplot as plt
import numpy as np


def graph(solution, routes):
    m = Model()
    m.build_model()
    plt.figure(figsize=(8, 6), dpi=80)
    xs = [x.x for x in m.allNodes]
    ys = [y.y for y in m.allNodes]
    ids = [x.id for x in m.allNodes]
    plt.scatter(xs, ys, c="blue", marker=".")
    plt.scatter(23.142, 11.736, c="black")
    color = iter(plt.cm.rainbow(np.linspace(0, 1, 6)))
    for route in routes:
        nodexs = [solution.all_nodes[id].x for id in route]
        nodeys = [solution.all_nodes[id].y for id in route]
        c = next(color)
        plt.plot(nodexs, nodeys, c= c)
    for x, y, id in zip(xs, ys, ids):
        plt.annotate(str(id), xy=(x,y))
    plt.gcf().set_size_inches((20, 20))
    plt.savefig("mygraphlined6.png")
