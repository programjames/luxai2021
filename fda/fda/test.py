
import numpy as np


def prepare_test(i):
    nx = i
    ny = i
    scores = np.zeros((nx, ny))
    scores[nx // 4, :] = 1
    resistances = np.ones(scores.shape)
    resistances[nx // 5, ny // 3:ny - 1 - ny // 3] = 2
    return -scores.T, resistances.T


def prepare_random(i):
    nx = i
    ny = i
    scores = np.random.rand(nx, ny) + 1
    resistances = np.random.rand(nx, ny) + 1
    return -scores.T, resistances.T


if __name__ == "__main__":

    import solver

    import seaborn as sns
    import matplotlib.pyplot as plt

    scores, resistances = prepare_test(50)
    poisson = solver.get_qtable(scores, resistances)
    p = solver.get_potential_dirichlet(scores, resistances)

    nx, ny = scores.shape
    x, y = np.meshgrid(range(nx), range(ny))

    fig = plt.figure(figsize=(10, 8))

    ax1 = fig.add_subplot(221)
    ax2 = fig.add_subplot(222)
    ax3 = fig.add_subplot(223)
    ax4 = fig.add_subplot(224)

    sns.heatmap(-scores, ax=ax1, cmap="vlag")
    sns.heatmap(resistances, ax=ax2, cmap="vlag")
    sns.heatmap(poisson, ax=ax3, cmap="vlag")
    sns.heatmap(p, ax=ax4, cmap="vlag")

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
    ax3.set_title("Potential (no resistance)")
    ax4.set_title("Potential (with resistance)")
    plt.show()
