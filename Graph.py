from Model import *
import matplotlib.pyplot as plt


def graph(solution, routes):
    m = Model()
    m.build_model()
    plt.figure(figsize=(8, 6), dpi=80)
    xs = [x.x for x in m.allNodes]
    ys = [y.y for y in m.allNodes]
    ids = [x.id for x in m.allNodes]
    plt.scatter(xs, ys, c="blue", marker=".")
    plt.scatter(23.142, 11.736, c="black")
    nodexs = [solution.all_nodes[id].x for id in routes[0]]
    nodeys = [solution.all_nodes[id].y for id in routes[0]]
    plt.plot(nodexs, nodeys)
    nodexs = [solution.all_nodes[id].x for id in routes[1]]
    nodeys = [solution.all_nodes[id].y for id in routes[1]]
    plt.plot(nodexs, nodeys, c="black")
    for x, y, id in zip(xs, ys, ids):
        plt.annotate(str(id), xy=(x,y))
    plt.gcf().set_size_inches((20, 20))
    plt.savefig("mygraphlined2.png")
