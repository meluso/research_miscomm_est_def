# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-10-18
@name: test_agent.py

This file tests the agent class.

"""

import model_agent as ag
from numpy.random import random_sample as rand

# Create an instance of an agent
a1 = ag.Agent(2,[0,3],0.5,"ackley")
print("Location = " + str(a1.location))
print("Neighbors = " + str(a1.neighbors))
print("Bound = " + str(a1.obj_bounds.xmax))
print("Estimate type = " + str(a1.est_type))
print("Objetive function type = " + a1.fn)

# Create a history vector for a set of 4 agents
for i in range(0,101):
    sys_vect = [rand(),rand(),rand(),rand()]
    a1.generate_history(sys_vect)
print("History = " + str(len(a1.history)) + " points")

# Set initial estimates for the agent
a1.initialize_estimates()
print("Current estimate = " + str(a1.curr_est.x))
print("Future estimate = " + str(a1.hist_med.x))

# Create an estimate
sys_vect = [1,5,3,2]
received_est = a1.generate_estimate(sys_vect)
print("Returned estimate = " + str(received_est))
print("Actual estimate = " + str(a1.curr_est.x))
