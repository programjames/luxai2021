from scipy.cluster.vq import vq, kmeans
from sklearn.metrics import silhouette_score
import numpy as np

import bfs


class Cluster(object):
    def update(self, game_map, player, city_locs, maxclust=5):
        positions = np.array([(u.pos.x, u.pos.y)
                              for u in player.units])
        distances = np.zeros((len(positions), len(positions)))
        # This certainly can be sped up with some kind of FFT
        for i, p in enumerate(positions):
            distances[i] = abs(p[0] - positions[:, 0]) + \
                abs(p[1] - positions[:, 1])

        self.form_clusters(positions, distances, maxclust=maxclust)

        self.make_bfs(game_map.width, game_map.height, city_locs)

    def form_clusters(self, data, distances, maxclust=5):
        if len(data) == 0:
            return

        maxclust = max(1, min(len(data) - 1, maxclust))

        data = data.astype("float64")
        sil = -np.inf
        for k in range(1, maxclust + 1):
            centers = kmeans(data, k)[0]
            labels = vq(data, centers)[0]
            if np.amax(labels) == 0:
                s = 0
            else:
                s = silhouette_score(distances, labels +
                                     1, metric="precomputed")
            if s < sil:
                break
            sil = s
            self.centers = centers.astype(int)
            self.centers = list(map(tuple, self.centers))
            self.labels = labels

    def make_bfs(self, width, height, city_locs):
        def found_criterion(x, y):
            return (x, y) in city_locs

        starting_locs = set()
        for center in self.centers:
            city_locs = bfs.search(found_criterion, width, height, [center])
            if len(city_locs) == 0:
                starting_locs.add(center)
            else:
                # Could eventually be min(city_locs, sum(distances_in_cluster))
                loc = min(city_locs)
                starting_locs.add(loc)

        self.bfs = bfs.BFS(width, height, starting_locs)

    def dir(self, x, y, can_stay=True, passable=None):
        return self.bfs.dir(x, y, can_stay, passable)


if __name__ == '__main__':
    from sklearn.datasets import make_blobs
    import matplotlib.pyplot as plt

    centers = [(-5, -5), (0, 0), (5, 5)]
    positions = make_blobs(100, centers=centers)[0]
    distances = np.zeros((len(positions), len(positions)))
    for i, p in enumerate(positions):
        distances[i] = abs(p[0] - positions[:, 0]) + \
            abs(p[1] - positions[:, 1])
    c = Cluster()
    c.form_clusters(positions, distances)
    plt.scatter(*positions.T, c=c.labels)
    plt.scatter(*c.centers.T, marker="s", color="black")
    plt.show()
