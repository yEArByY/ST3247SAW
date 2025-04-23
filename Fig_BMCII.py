#@title Click to Expand/Collapse

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

mus=[]
Ls=[]
smoothing=100
N=100000
for L in range(20,500,20):
  sub_mus=[]
  for i in range(smoothing):
    Is,Ps,Qs=generate_self_avoiding_walk(L)
    Ps = np.array(Ps)
    Qs = np.array(Qs)

    Rs = Ps / Qs  # Element-wise division

    normalized_weights = Rs #/ np.sum(Rs)
    proportion_estimate = np.mean(np.array(Is) * normalized_weights)
    cL=proportion_estimate * 4**L
    targetmu1=cL**(1/L)
    sub_mus.append(targetmu1)


  targetmu=np.mean(sub_mus)

  Ls.append(L)
  mus.append(targetmu)

#visualise
import matplotlib.pyplot as plt
plt.plot(Ls,mus)
plt.show()


