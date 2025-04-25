"""
Uses a DFS algorithm to deterministically count all SAWs
"""

def count_self_avoiding_walks(x, y, depth, L, visited):
    if (x, y) in visited:
        return 0  # Already visited, invalid path
    if depth == L:
        return 1  # Reached the required length

    # Mark the current position as visited
    visited.add((x, y))

    # Define movement directions: up, right, down, left
    moves = [(0, 1), (1, 0), (0, -1), (-1, 0)]
    total_paths = 0

    # Recursively explore all 4 directions
    for dx, dy in moves:
        total_paths += count_self_avoiding_walks(x + dx, y + dy, depth + 1, L, visited)

    # Backtrack (unmark position)
    visited.remove((x, y))

    return total_paths



# Wrapper function to start DFS
def distinct_self_avoiding_walks(L):
    return count_self_avoiding_walks(0, 0, 0, L, set())



# Example usage:
L = 15  # Change L as needed
print(distinct_self_avoiding_walks(L))
