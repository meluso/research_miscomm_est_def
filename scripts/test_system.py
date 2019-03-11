# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-10-21
@name: test_system.py

This file tests the system class.

"""

import model_system as sy
import matplotlib.pyplot as plt
import networkx as nx
import datetime as dt

# Start timer
t_start = dt.datetime.now()

# Generate a system with n nodes
n = 1000
s1 = sy.System(n,"sphere",0.9,"current_always")

# Plot the system
options = {
        'node_color': 'red',
        'node_size': 15,
        'width': 1
        }
nx.draw_kamada_kawai(s1.graph, **options)
plt.savefig("network_graph.tif", format='tif', dpi=250)
plt.savefig("network_graph.eps", format='eps', dpi=250)
plt.show()

#degree histogram
hist = [float(x)/n for x in nx.degree_histogram(s1.graph)]        

# Create a linear plot of the degree distribution
#plt.plot(hist, color='b',marker=".",ls="none")
#plt.show()

# Create a logarithmic plot of the degree distribution
plt.loglog(hist, color='b',marker=".",ls="none")
plt.ylabel("Fraction of Nodes")
plt.xlabel("Artifact Degree")
plt.savefig("degree_distribution.tif", format='tif', dpi=250)
plt.savefig("degree_distribution.eps", format='eps', dpi=250)
plt.show()

# 

# Run the system
results = s1.run()

# Plot the results
plt.plot(results.perf_system)
plt.xlabel("Design Cycle")
plt.ylabel("System Performance")
#plt.semilogy(results.perf_system)
plt.show()

# Stop timer
t_stop = dt.datetime.now()
print(t_stop - t_start)
