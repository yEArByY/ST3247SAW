#4 this basically generates a self avoiding random walk
import numpy as np

def generate_self_avoiding_walk(L):
    visited = [(0, 0)]  # List to track visited positions (ordered)
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
        visited.append((x, y))  # Mark new position as visited
        p*=1/4
        q*=1/(len(possible_steps))
        #print(q)

    #print(f"Terminating regularly with length {len(visited)}, visited places: {visited}")
    return 1,p,q

def rand_walk_estimate(L,N):
    Is=[]
    Ps=[]
    Qs=[]
    Rs=[]
    for i in range(N):
        I,p,q=generate_self_avoiding_walk(L)
        Is.append(I)
        Ps.append(p)
        Qs.append(q)
    
    Ps = np.array(Ps)
    Qs = np.array(Qs)

    Rs = Ps / Qs  # Element-wise division
    normalized_weights = Rs #/ np.sum(Rs)
    proportion_estimate = np.mean(np.array(Is) * normalized_weights)

    return proportion_estimate * 4**L

rand_walk_estimate(8,10000)


mus=[]
Ls=[]
N = 1000 #number of repeates
for L in range(10,500,20):
  Ls.append(L)
  cL = rand_walk_estimate(L,N)
  #print(cL)
  #print(L)
  #print(cL**(1/L))
  mus.append(cL**(1/L))

#visualise
import matplotlib.pyplot as plt
plt.plot(Ls,mus)
plt.show()
