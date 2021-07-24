import numpy as np
from scipy.fft import dctn, idctn
from scipy.sparse.linalg import LinearOperator, gmres
import sys

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
Uses the Woodbury matrix addition formula to solve the equation

    (L + Iγ)p = f, where γ = 4-4r.

The Woodbury equation gives us

    (L + Iγ)⁻¹ = L⁻¹ - L⁻¹(L⁻¹ + Iγ⁻¹)⁻¹L⁻¹

As  L⁻¹x = solve_poisson(x), and (Iγ⁻¹)x = x/γ, we can use GMRES to quickly
solve

    (L⁻¹ + Iγ⁻¹)z = L⁻¹f

Our answer is then just L⁻¹f - L⁻¹z.


References: https://en.wikipedia.org/wiki/Woodbury_matrix_identity#Inverse_of_a_sum
            https://hal.archives-ouvertes.fr/hal-02010640/document
"""


def get_potential(f, r, tol=1e-3, max_iters=10):
    f -= np.mean(f)
    gamma = 4 * (1 - r)
    gamma[abs(gamma) < 1e-9] = 1e-9

    def W(v):
        v = v.reshape(f.shape)
        return solve_poisson(v) + v / gamma
    n2 = np.prod(f.shape)
    L = LinearOperator(shape=(n2, n2), matvec=W)
    u = solve_poisson(f)
    z, _ = gmres(L, u.flatten(), tol=tol, maxiter=max_iters)
    z = z.reshape(f.shape)
    return u - solve_poisson(z)
