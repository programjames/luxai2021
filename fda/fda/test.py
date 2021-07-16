import solver
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt


def prepare_test(i):
    nx = i
    ny = i
    scores = np.ones((nx, ny))
    for x in range(nx):
        for y in range(ny):
            if 1 / 25 * ((nx - 1)**2 + (ny - 1)**2) > \
                    (nx / 2 - 0.5 - x)**2 + (ny / 2 - 0.5 - y)**2:
                scores[x, y] = 2
    resistances = np.ones(scores.shape)
    resistances[2 * nx // 3, ny // 4:ny - ny // 4] = 2
    return -scores.T, resistances.T


def prepare_random(i):
    nx = i
    ny = i
    scores = np.random.rand(nx, ny)
    resistances = np.random.rand(nx, ny) * 5 + 1
    return -scores.T, resistances.T


scores, resistances = prepare_test(51)
poisson = solver.solve_poisson(scores)
p = solver.get_potential(scores, resistances)

nx, ny = scores.shape
x, y = np.meshgrid(range(nx), range(ny))


fig = plt.figure(figsize=(10, 8))


ax1 = fig.add_subplot(221)
ax2 = fig.add_subplot(222)
ax3 = fig.add_subplot(223)
ax4 = fig.add_subplot(224)
sns.heatmap(-scores, ax=ax1)
sns.heatmap(resistances, ax=ax2)
sns.heatmap(poisson, ax=ax3)
sns.heatmap(p, ax=ax4)

# 3D graphs
# from mpl_toolkits.mplot3d import Axes3D
# ax1 = fig.add_subplot(221, projection='3d')
# ax2 = fig.add_subplot(222, projection='3d')
# ax3 = fig.add_subplot(223, projection='3d')
# ax4 = fig.add_subplot(224, projection='3d')
# ax1.plot_surface(x, y, -scores)
# ax2.plot_surface(x, y, resistances)
# ax3.plot_surface(x, y, poisson)
# ax4.plot_surface(x, y, p)

ax1.set_title("Scores")
ax2.set_title("Resistances")
ax3.set_title("Potentials (no resistance)")
ax4.set_title("Potentials (with resistance)")
plt.show()
