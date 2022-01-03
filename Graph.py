import matplotlib.pyplot as plt


def graph(solution, routes):
    plt.figure(figsize=(8, 6), dpi=80)
    xs = [x.x for x in solution.all_nodes]
    ys = [y.y for y in solution.all_nodes]
    ids = [x.ID for x in solution.all_nodes]
    plt.scatter(xs, ys, c="blue", marker=".")
    plt.scatter(23.142, 11.736, c="black")
    plt.scatter(0, 0, c="black")
    c = iter(["blue", "yellow", "red", "brown", "black", "pink"])
    for route in routes:
        node_xs = [solution.all_nodes[ID].x for ID in route.nodes]
        node_ys = [solution.all_nodes[ID].y for ID in route.nodes]
        plt.plot(node_xs, node_ys, c=next(c))
    for x, y, ID in zip(xs, ys, ids):
        plt.annotate(str(ID), xy=(x, y))
    plt.gcf().set_size_inches((30, 30))
    leg = ["Route " + str(i) + " d: " + str(solution.routes[i].truck.duration_left)
           + " c: " + str(solution.routes[i].truck.capacity_left) + " p: " + str(solution.routes[i].profit)
           for i in range(len(solution.routes))] + [solution.total_profit] \
           + [str(sum(solution.routes[i].profit for i in range(len(solution.routes))))]
    plt.legend(leg, loc='lower right')
    ind = 0
    # plt.gca().add_patch(plt.Circle((solution.all_nodes[ind].x, solution.all_nodes[ind].y), 50, fill=False))
    # plt.gca().add_patch(plt.Circle((solution.all_nodes[ind].x, solution.all_nodes[ind].y), 25, fill=False))
    plt.gca().add_patch(plt.Circle((solution.all_nodes[ind].x, solution.all_nodes[ind].y), 15, fill=False))
    plt.savefig("test.png")
    plt.close()
