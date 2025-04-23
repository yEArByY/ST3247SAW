#@title Click to Expand/Collapse

import matplotlib.pyplot as plt
import numpy as np
import random

# 2D lattice directions
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def fast_perm_mu_estimate(L, num_samples=10000, max_clones=50):
    """
    Estimate the connective constant mu for a single walk length L using a fast PERM-like approach.
    """
    total_weight = 0
    total_extension_weight = 0

    for _ in range(num_samples):
        walk = [(0, 0)]
        visited = set(walk)
        weight = 1
        success = True

        for _ in range(L):
            x, y = walk[-1]
            options = [(x + dx, y + dy) for dx, dy in directions if (x + dx, y + dy) not in visited]
            m = len(options)

            if m == 0:
                success = False
                break

            weight *= m
            next_pos = random.choice(options)
            walk.append(next_pos)
            visited.add(next_pos)

            # light enrichment: clone if weight too high
            if weight > 10:
                for _ in range(min(max_clones, m)):
                    clone_walk = walk[:]
                    clone_visited = visited.copy()
                    total_weight += weight
                    x_clone, y_clone = clone_walk[-1]
                    clone_options = [(x_clone + dx, y_clone + dy) for dx, dy in directions if (x_clone + dx, y_clone + dy) not in clone_visited]
                    total_extension_weight += weight * len(clone_options)

        if success:
            total_weight += weight
            x, y = walk[-1]
            options = [(x + dx, y + dy) for dx, dy in directions if (x + dx, y + dy) not in visited]
            total_extension_weight += weight * len(options)

    if total_weight == 0:
        return None

    return total_extension_weight / total_weight

# Estimate mu for various lengths
L_values = list(range(20, 500, 20))
mu_estimates = [fast_perm_mu_estimate(L, num_samples=10000) for L in L_values]

# Plotting
plt.figure(figsize=(10, 6))
plt.plot(L_values, mu_estimates, marker='o', color='blue', label='Estimated $\hat{\mu}_L$')
plt.axhline(y=2.638, color='r', linestyle='--', label='Expected $\mu$ for 2D SAW')
plt.xlabel("Walk Length $L$")
plt.ylabel("Estimated Connective Constant $\hat{\mu}_L$")
plt.title("Behavior of $\hat{\mu}_L$ vs Walk Length $L$ using Fast PERM")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()

