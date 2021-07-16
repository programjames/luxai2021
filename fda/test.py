import fda
import numpy as np

import seaborn as sns
import matplotlib.pyplot as plt


def prepare_test(i):
    nx = i
    ny = i
    scores = np.ones((nx, ny))
    for x in range(nx):
        for y in range(ny):
            scores[x, y] = -np.sqrt(((nx - 1) / 2 - x)
                                    ** 2 + ((ny - 1) / 2 - y)**2)

    resistances = np.ones(scores.shape)
    for x in range(nx // 2, 5 * nx // 6):
        resistances[x, :] = 6
    return scores, resistances


scores, resistances = prepare_test(30)
potential, error = fda.get_potential(scores, resistances)
print(error)
# sns.heatmap(scores, linewidth=0)
# plt.show()
# sns.heatmap(resistances, linewidth=0)
# plt.show()
sns.heatmap(potential, linewidth=0)
plt.show()
