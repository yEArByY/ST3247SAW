
#generating "repeated" number of samples and calculating the proportion of these that are self avoiding

import numpy as np

def monte_carlo_self_avoiding_proportion(repeated, L):
    successful_walks = 0  # Tally for self-avoiding walks

    for _ in range(repeated):
        visited = {(0, 0)}  # Set for tracking visited positions
        x, y = 0, 0  # Start at (0,0)

        for _ in range(L):
            ####################################################################
            i= np.random.choice([0,1,2,3])  # Random step in x and y
            dx, dy = [(0, 1), (1, 0), (0, -1), (-1, 0)][i]
            x, y = x + dx, y + dy  # Update position

            if (x, y) in visited:
                break  # Walk is not self-avoiding, terminate early

            visited.add((x, y))  # Mark position as visited
        else:
            # If we complete L steps without breaking, it's a self-avoiding walk
            successful_walks += 1

    return successful_walks / repeated  # Proportion of self-avoiding walks



# Example usage:
repeated = 10000  # Number of Monte Carlo trials
L = 4  # Length of each walk
cL=monte_carlo_self_avoiding_proportion(repeated, L) * 4**L
cL1=monte_carlo_self_avoiding_proportion(repeated, L+1) * 4**(L+1)
mu=cL1/cL
print(f"Estimated mu for L={L}: {mu}")
