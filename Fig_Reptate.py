#@title Click to Expand/Collapse
import random
import numpy as np
import copy

#Add importance sampling to mcmc, try to express new distribution that is better fit as proposal density
###################################################################################################
def self_avoiding_random_walk(L):
    visited = [(0, 0)]  # List to track visited positions (ordered)
    x, y = 0, 0  # Start at (0,0)
    ps,qs=[1],[1]
    phi=0
    for i in range(L):
        possible_steps = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        possible_steps = [(dx, dy) for dx, dy in possible_steps if (x + dx, y + dy) not in visited]

        if not possible_steps:
            return phi,ps,qs,visited #not a succussful walk

        dx, dy = possible_steps[np.random.randint(len(possible_steps))]
        x, y = x + dx, y + dy
        visited.append((x, y))
        ps.append(1/4)
        qs.append( 1/(len(possible_steps)) )

    phi=1
    return phi,ps,qs,visited #successful walk

#this can result in self avoiding walks of different lengths.
#the mcmc approach is just to make use of the successful fragments of successful walks...or make use of the successful fragments of unsuccessful walks.

def propose_new_walk(I,ps,qs,path,L):
    """
    Propose a new self-avoiding walk by altering the current path slightly.
    This could involve shifting an endpoint or modifying a segment of the path.
    """
    new_path = copy.deepcopy(path)
    new_ps = copy.deepcopy(ps)
    new_qs = copy.deepcopy(qs)

    ###################################################################choosing to extend/reptate: successfulness, length<=4?

    # choice = random.choice(["extend", "reptate"])
    if I==0:
      choice="extend" #SMC?
    else:
      choice="reptate" #Pivot?

    ##############################################################################################################################
    ## Attempt to extend the walk from the second to endpoint, until success walk
    if choice == "extend":

      return 0,new_ps,new_qs


    elif choice == "reptate":
      ##################################rewalk parts of a successful walk
        # Randomly choose a pivot
        if len(new_path) > 2:
            segment_start = random.randint(1, len(new_path) - 2)
            new_path = new_path[:segment_start]
            new_ps = new_ps[:segment_start]
            new_qs = new_qs[:segment_start]

            ########################################################just walk until no possible steps
            while len(new_path) < len(path):
                current_position = new_path[-1]
                moves = [(0, 1), (0, -1), (1, 0), (-1, 0)]
                candidates = [
                    (current_position[0] + move[0], current_position[1] + move[1])
                    for move in moves
                    if (current_position[0] + move[0], current_position[1] + move[1]) not in new_path
                ]
                ########################new walk fails, return original I,p,q
                if not candidates:
                  # I,p,q = 0,np.prod(ps),np.prod(qs)
                  return 0,ps,qs

                #######################
                next_position = random.choice(candidates)
                new_path.append(next_position)
                new_ps.append(1/4)
                new_qs.append(1/len(candidates))

            #################calculate and also return probability of new walk
            # newI,newp,newq=1,np.prod(new_ps),np.prod(new_qs)
            return 1,new_ps,new_qs





def mcmc_self_avoiding_random_walk(L, iterations):
    # Start with an initial self-avoiding walk
    count = 0
    Is=[]
    Ps=[]
    Qs=[]

    while count < iterations:#number of recorded walks
      I,ps,qs,path = self_avoiding_random_walk(L)


      p=np.prod(ps)
      q=np.prod(qs)

      #if not finished walk, modify walk
      #if finished walk, append walk and reptate walk
      if I==1:
        Is.append(I)
        Ps.append(p)
        Qs.append(q)
        count += 1
      ###########################################under certain probability, activate the proposed path
      #current activation happens every iteration.
      new_I, new_ps, new_qs = propose_new_walk(I,ps,qs,path,L)
      count += 1

      new_p=np.prod(new_ps)
      new_q=np.prod(new_qs)

      Is.append(new_I)
      Ps.append(new_p)
      Qs.append(new_q)

    return Is,Ps,Qs,path

#Wrapper function with IS
# L = 300
# N = 10000

# Is,Ps,Qs,path=mcmc_self_avoiding_random_walk(L, N)

# # Convert Ps and Qs to NumPy arrays for element-wise division
# Ps = np.array(Ps)
# Qs = np.array(Qs)

# Rs = Ps / Qs  # Element-wise division

# normalized_weights = Rs #/ np.sum(Rs)
# proportion_estimate = np.mean(np.array(Is) * normalized_weights)
# print("MCMC results")
# print(proportion_estimate)
# cL=proportion_estimate * 4**L
# print(cL)
# print(cL**(1/L))

mus=[]
Ls=[]
N=10000
for L in range(20,500,20):
  Is,Ps,Qs,path=mcmc_self_avoiding_random_walk(L, N)
  Ps = np.array(Ps)
  Qs = np.array(Qs)

  Rs = Ps / Qs  # Element-wise division

  normalized_weights = Rs #/ np.sum(Rs)
  proportion_estimate = np.mean(np.array(Is) * normalized_weights)
  cL=proportion_estimate * 4**L
  targetmu=cL**(1/L)
  Ls.append(L)
  mus.append(targetmu)

#visualise
import matplotlib.pyplot as plt
plt.plot(Ls,mus)
plt.show()