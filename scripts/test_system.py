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
import collections
import datetime as dt

# Start timer
t_start = dt.datetime.now()

# Generate a system
s1 = sy.System(100,"ackley",1,"future_always")

# Plot the system
options = {
        'node_color': 'black',
        'node_size': 5,
        'width': 1
        }
#nx.draw(s1.graph, **options)
nx.draw_kamada_kawai(s1.graph, **options)
plt.show()

# Graph the degree distribution of the system
degree_sequence = sorted([d for n, d in s1.graph.degree()], reverse = True)
degree_count = collections.Counter(degree_sequence)
deg, cnt = zip(*degree_count.items())
plt.loglog(deg, cnt, color='b')
plt.title("Degree Histogram")
plt.ylabel("Frequency")
plt.xlabel("Artifact Degree")
plt.show()
plt.savefig("degree_distribution.svg")

# Run the system
results = s1.run()

# Plot the results
plt.plot(results.perf_system)
#plt.semilogy(results.perf_system)
plt.show()

# Stop timer
t_stop = dt.datetime.now()
print(t_stop - t_start)