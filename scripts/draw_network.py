# -*- coding: utf-8 -*-
"""
Created on Fri Jan 04 13:42:59 2019

@author: Juango the Blue
"""

import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
import matplotlib.image as mpimg
import model_system as sy
    

# Generate a system
s1 = sy.System(100,"sphere",1,"future_always")

# Sort the system graph
Q = nx.algorithms.community.greedy_modularity_communities(s1.graph)

# Compile sorted order into a single 'order' vector
order = [] # Initialize the order vector
for i in range(len(Q)): # Sort through the communities of Q
    
    # Extract the current community i from Q
    community = sorted(Q[i])
    
    # Sort through the members of the selected community
    for j in range(len(community)):
        
        # Append the entry to the end of the order vector
        order.append(community[j])

# Convert to numpy matrix
adjacency_matrix = nx.to_numpy_matrix(s1.graph, dtype=np.bool, nodelist=order)

# Create figure for adjacency matrix with axes
fig, ax = plt.subplots(figsize=[5,5])
im = ax.imshow(adjacency_matrix,cmap="Greys")
plt.axis("on")

# Save and show the figure
plt.savefig("adjacency_matrix.eps",dpi=250)
plt.savefig("adjacency_matrix.tif",dpi=250)
plt.show()