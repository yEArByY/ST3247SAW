#@title Click to Expand/Collapse
import random
import numpy as np
import matplotlib.pyplot as plt

DIRS = [(1,0), (-1,0), (0,1), (0,-1)]

def pivot_transform():
    """Return a random symmetry operation (rotation/reflection)."""
    ops = [
        lambda x, y: (x, y),
        lambda x, y: (-x, y),
        lambda x, y: (x, -y),
        lambda x, y: (-x, -y),
        lambda x, y: (y, x),
        lambda x, y: (-y, x),
        lambda x, y: (y, -x),
        lambda x, y: (-y, -x)
    ]
    return random.choice(ops)

def pivot_move(path):
    """Attempt a pivot move on the SAW."""
    if len(path) < 3:
        return path
    pivot_idx = random.randint(1, len(path) - 2)
    pivot = path[pivot_idx]
    transform = pivot_transform()

    before = path[:pivot_idx + 1]
    rel_after = [(x - pivot[0], y - pivot[1]) for x, y in path[pivot_idx + 1:]]
    after = [(transform(x, y)[0] + pivot[0], transform(x, y)[1] + pivot[1]) for x, y in rel_after]
    new_path = before + after

    if len(set(new_path)) == len(new_path):  # still self-avoiding
        return new_path
    return path

def random_saw(n):
    """Generate a self-avoiding walk via random growth."""
    path = [(0, 0)]
    visited = {path[0]}
    while len(path) < n:
        x, y = path[-1]
        options = [(x + dx, y + dy) for dx, dy in DIRS if (x + dx, y + dy) not in visited]
        if not options:
          return random_saw(n)  # Restart if stuck
        step = random.choice(options)
        path.append(step)
        visited.add(step)
    return path

def estimate_mu_via_pivot(n=300, n_steps=10000):
    path = random_saw(n)
    mu_samples = []

    for _ in range(n_steps):
        path = pivot_move(path)

        # Attempt all possible 1-step extensions
        x, y = path[-1]
        visited = set(path)
        valid_extensions = sum(
            (x + dx, y + dy) not in visited for dx, dy in DIRS
        )
        mu_samples.append(valid_extensions)

    mu_est = np.mean(mu_samples)
    return mu_est, mu_samples


mus=[]
Ls=[]
for n in range(20, 300, 20):
  targetmu=[]
  for i in range(20):
    mu_est, _ = estimate_mu_via_pivot(n=n, n_steps=10000)
    targetmu.append(mu_est)

  targetmu1=np.mean(targetmu)
  mus.append(targetmu1)
  Ls.append(n)

plt.plot(Ls, mus)
plt.title("Estimated μ vs. Walk Length (Pivot)")
plt.xlabel("Walk Length (L)")
plt.ylabel("Estimated μ")

