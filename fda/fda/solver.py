import numpy as np
from scipy.fft import dctn, idctn

""" solve_poisson(f)

Solves the Poisson equation

    ∇²p = f

using the finite difference method with Neumann boundary conditions.

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
    return potential / 2


""" get_potential(f, r, tol=1e-2, max_iters=10)
Uses the Woodbury matrix subtraction formula to solve the equation

    (L - Iγ)p = f, where γ = 4-4r.

The Woodbury equation gives us

    (L - Iγ)⁻¹ = ∑ (L⁻¹γ)ⁿ L⁻¹u.

As  L⁻¹u = solve_poisson(u), and (Iγ)u = γ⊙u, we can use the following iteration:

    1. p = solve_poisson(f), k = p.copy()
    2. k = solve_poisson(γ*k)
    3. p += k
    4. Repeat steps (2) and (3) until convergence.


References: https://en.wikipedia.org/wiki/Woodbury_matrix_identity#Inverse_of_a_sum
            https://hal.archives-ouvertes.fr/hal-02010640/document
"""


def get_potential(f, r, tol=1e-2, max_iters=10):
    gamma = 4 - 4 * r
    p = solve_poisson(f)
    p -= np.mean(p)
    k = np.copy(p)
    prev_k = k
    rs = []
    for i in range(max_iters):
        k = solve_poisson(k * gamma)
        k /= np.prod(f.shape)  # np.amax(abs(k))
        p += k
        m = np.amax(abs(p))
        if m == 0:
            break
        p /= m
        k /= m
        if np.amax(abs(k - prev_k)) < tol:
            break
        prev_k = k
    return p
