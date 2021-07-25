import solver
import numpy as np
import time

from test import prepare_test


t = time.time()
outer_v = None
for i in range(100):
    s, r = prepare_test(50)
    p = solver.get_potential_dirichlet(s, r, tol=1e-3, outer_v=outer_v)
    outer_v = [(p.flatten(), s.flatten())]
print(time.time() - t)
