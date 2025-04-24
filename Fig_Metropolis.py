import numpy as np
import matplotlib.pyplot as plt
import random

# Define 2D lattice directions
directions = [(1, 0), (-1, 0), (0, 1), (0, -1)]

def propose_pivot(walk):
    """Propose a pivot move on the walk."""
    if len(walk) < 3:
        return walk
    pivot_idx = random.randint(1, len(walk) - 2)
    pivot_point = walk[pivot_idx]
    tail = walk[pivot_idx + 1:]

    # Symmetries (rotations/reflections)
    symmetries = [
        lambda x, y: (-y, x),    # 90°
        lambda x, y: (-x, -y),   # 180°
        lambda x, y: (y, -x),    # 270°
        lambda x, y: (x, -y),    # Reflect X
        lambda x, y: (-x, y),    # Reflect Y
        lambda x, y: (x, y)      # Identity
    ]
    transform = random.choice(symmetries)

    new_tail = [(
        transform(x - pivot_point[0], y - pivot_point[1])[0] + pivot_point[0],
        transform(x - pivot_point[0], y - pivot_point[1])[1] + pivot_point[1]
    ) for (x, y) in tail]

    new_walk = walk[:pivot_idx + 1] + new_tail
    return new_walk

def count_extensions(walk):
    """Count number of valid (non-colliding) next steps."""
    x, y = walk[-1]
    visited = set(walk)
    return sum((x + dx, y + dy) not in visited for dx, dy in directions)

def metropolis_hastings_mu(L, steps=5000):
    """Estimate mu using Metropolis-Hastings with extension-based weighting."""
    walk = [(i, 0) for i in range(L + 1)]
    mus = []

    for _ in range(steps):
        proposed = propose_pivot(walk)
        if len(set(proposed)) < len(proposed):
            continue  # Reject non-self-avoiding

        e_current = count_extensions(walk)
        e_proposed = count_extensions(proposed)
        if e_current == 0:
            e_current = 1e-6  # Avoid div-by-zero
        accept_prob = min(1, e_proposed / e_current)

        if random.random() < accept_prob:
            walk = proposed

        mus.append(count_extensions(walk))

    return np.mean(mus)

# Run for various L and plot
L_vals = list(range(20, 500, 20))
mu_estimates = [metropolis_hastings_mu(L, steps=10000) for L in L_vals]

# Plot
plt.figure(figsize=(10, 6))
plt.plot(L_vals, mu_estimates, marker='o', label='Estimated $\hat{\\mu}_L$ (MH)')
plt.axhline(2.638, linestyle='--', color='red', label='Expected $\mu$ (2D SAW)')
plt.xlabel("Walk Length $L$")
plt.ylabel("Estimated $\hat{\\mu}_L$")
plt.title("Metropolis-Hastings Estimation of $\mu$ vs Walk Length $L$")
plt.legend()
plt.grid(True)
plt.tight_layout()
plt.show()
