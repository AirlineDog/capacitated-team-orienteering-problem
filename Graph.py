from Model import *
import matplotlib.pyplot as plt

m = Model()
m.build_model()
plt.figure(figsize=(8, 6), dpi=80)
xs = [x.x for x in m.allNodes]
ys = [y.y for y in m.allNodes]
ids = [x.id for x in m.allNodes]
plt.scatter(xs, ys, c="blue", marker=".")
plt.scatter(23.142, 11.736, c="black")
plt.plot(xs, ys, c="black")
for x, y, id in zip(xs, ys, ids):
    plt.annotate(str(id), xy=(x,y))
plt.gcf().set_size_inches((20, 20))
plt.savefig("mygraphlined.png")
print()