#@title Click to Expand/Collapse
import random

directions = [(1,0), (-1,0), (0,1), (0,-1)]

def rosenbluth_walk(n):
    path = [(0, 0)]
    visited = set(path)
    weight = 1

    for _ in range(n):
        x, y = path[-1]
        options = [(x + dx, y + dy) for dx, dy in directions if (x + dx, y + dy) not in visited]

        m = len(options)
        if m == 0:
            return None, 0  # Trapped


        weight *= m
        next_pos = random.choice(options)
        path.append(next_pos)
        visited.add(next_pos)

    return path, weight

def estimate_mu_rosenbluth(n=20, trials=10000):
    total_weight_n = 0
    total_weight_np1 = 0

    for _ in range(trials):
        walk, w_n = rosenbluth_walk(n)
        if walk is None:
            continue
        total_weight_n += w_n

        # Try extending this walk by 1 step
        x, y = walk[-1]
        visited = set(walk)
        options = [(x + dx, y + dy) for dx, dy in directions if (x + dx, y + dy) not in visited]
        m_ext = len(options)
        total_weight_np1 += w_n * m_ext  # Importance weighted

    if total_weight_n == 0:
        return None

    mu_est = total_weight_np1 / total_weight_n
    return mu_est

# Run the estimator
mu1 = estimate_mu_rosenbluth(n=20, trials=50000)
print(f"Estimated μ (Rosenbluth): {mu1:.5f}")

mu2 = estimate_mu_rosenbluth(n=300, trials=100000)
print(f"Estimated μ (Rosenbluth): {mu2:.5f}")
