import numpy as np
from numpy.linalg import norm
from scipy.fft import dctn, idctn, fftn, ifftn
from scipy import interpolate

if __package__ == "":
    from lux.game_constants import GAME_CONSTANTS
else:
    from lux.game_constants import GAME_CONSTANTS

""" get_potential(scores)
Takes the energy values and returns how much potential each square has by solving
the discrete poisson equation.


References: https://elonen.iki.fi/code/misc-notes/neumann-cosine/
            https://scicomp.stackexchange.com/questions/12913/poisson-equation-with-neumann-boundary-conditions
"""


def solve_poisson(f):
    nx, ny = f.shape

    # Transform to DCT space
    dct = dctn(f, type=1)

    # Divide by magical factors
    cx = np.cos(np.pi * np.arange(nx) / (nx - 1))
    cy = np.cos(np.pi * np.arange(ny) / (ny - 1))
    f = np.add.outer(cx, cy) - 2

    np.divide(dct, f, out=dct, where=f != 0)
    dct[f == 0] = 0

    # Return to normal space
    potential = idctn(dct, type=1)
    return -potential


def norm(m):
    return np.linalg.norm(m, ord=np.inf)


def get_potential(scores, resistances, tol=1e-3, max_iters=20):
    scores /= norm(scores)**0.5
    errors = []
    potential = solve_poisson(scores)
    potential /= norm(potential)
    for i in range(max_iters - 1):
        p = solve_poisson((scores + 4 * (1 - resistances) * potential))
        p /= norm(p)
        error = norm(p - potential)
        if error < tol:
            return p, error

        if i >= 2:
            errors = errors[1:] + [error]
        else:
            errors.append(error)
        potential = p

    return p, error
