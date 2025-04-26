#4 this basically generates a self avoiding random walk
import numpy as np

def generate_self_avoiding_walk(L):
    visited = set([(0, 0)])  # List to track visited positions (ordered)
    x, y = 0, 0  # Start at (0,0)
    p,q=1,1
    for i in range(L):
        possible_steps = [(0, 1), (1, 0), (0, -1), (-1, 0)]  # Up, Right, Down, Left
        # Remove steps that would lead to a previously visited position
        possible_steps = [(dx, dy) for dx, dy in possible_steps if (x + dx, y + dy) not in visited]
        if not possible_steps:
            #print(f"Terminating early with length {len(visited)}, visited places: {visited}")
            return 0,p,q  # No valid moves left, terminate early

        # Randomly, uniformly select a valid step
        dx, dy = possible_steps[np.random.randint(len(possible_steps))]
        x, y = x + dx, y + dy  # Update position
        visited.add((x, y))  # Mark new position as visited
        p*=1/4
        q*=1/(len(possible_steps))
        #print(q)

    #print(f"Terminating regularly with length {len(visited)}, visited places: {visited}")
    return 1,p,q


# Example usage:
L = 10  # Length of the walk
# print(generate_self_avoiding_walk(L))
#expect a 2d array length of L+1, with the first entry ebing (0,0)


#Discuss how can this procedure be used to estimate the number of self-avoiding walks of a given length L

#Wrapper function to generate self-avoiding walks
Is=[]
Ps=[]
Qs=[]
Rs=[]
N=10000
L=10
for i in range(N):
    I,p,q=generate_self_avoiding_walk(L)
    Is.append(I)
    Ps.append(p)
    Qs.append(q)

# Convert Ps and Qs to NumPy arrays for element-wise division
Ps = np.array(Ps)
Qs = np.array(Qs)

Rs = Ps / Qs  # Element-wise division

print(np.sum(Is))
normalized_weights = Rs #/ np.sum(Rs)
proportion_estimate = np.mean(np.array(Is) * normalized_weights)
print(proportion_estimate)
print(proportion_estimate * 4**L)
