# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-10-18
@name: test_agent.py

This file tests the agent class.

"""

import model_agent as ag
from numpy.random import random_sample as rand
import matplotlib.pylab as plt
import doe_lhs as doe

# Create an instance of an agent
a1 = ag.Agent(2,[0,3],0.5,"ackley","best_est")
print("Location = " + str(a1.location))
print("Neighbors = " + str(a1.neighbors))
print("Bound = " + str(a1.obj_bounds.xmax))
print("Estimate type = " + str(a1.est_type))
print("Objective function type = " + a1.fn)

# Create a history vector for a set of 4 agents
sys_vect = [ag.Obj_Eval() for i in range(4)]
hypercube = doe.lhs(4,101)

# Get bounds from agent
min_val = a1.obj_bounds.xmin
max_val = a1.obj_bounds.xmax
            
# Scale all of the agents' samples to that range
for i in range(4):
    for h in range(101):
        hypercube[h][i] = min_val + (max_val - min_val)*hypercube[h][i]

# Generate history
for h in range(0,101):
    lhs_vect = hypercube[h][:]
    sys_vect[2] = a1.rand_hist_init(lhs_vect)
    est_vect = [ag.Obj_Eval(rand(),rand()),
                ag.Obj_Eval(rand(),rand()),
                sys_vect[2],
                ag.Obj_Eval(rand(),rand())]
    a1.save_history(est_vect)
        
print("History = " + str(len(a1.history)) + " points")

# Set initial estimates for the agent
print("--Initial estimate--")
a1.initialize_estimates()
print("Current estimate = f(" + str(a1.curr_est.x) + ") = " + str(a1.curr_est.fx))
print("Future estimate = f(" + str(a1.hist_med.x) + ") = " + str(a1.hist_med.fx))

# Create an estimate
print("--1st updated estimate--")
sys_vect = [ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand())]
received_est = a1.generate_estimate(sys_vect)
print("Returned estimate = f(" + str(received_est.x) + ") = " + str(received_est.fx))
print("Current estimate = f(" + str(a1.curr_est.x) + ") = " + str(a1.curr_est.fx))
print("Future estimate = f(" + str(a1.hist_med.x) + ") = " + str(a1.hist_med.fx))

# Create an estimate
print("--2nd updated estimate--")
sys_vect = [ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand())]
received_est = a1.generate_estimate(sys_vect)
print("Returned estimate = f(" + str(received_est.x) + ") = " + str(received_est.fx))
print("Current estimate = f(" + str(a1.curr_est.x) + ") = " + str(a1.curr_est.fx))
print("Future estimate = f(" + str(a1.hist_med.x) + ") = " + str(a1.hist_med.fx))

# Create an estimate
print("--3rd updated estimate--")
sys_vect = [ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand())]
received_est = a1.generate_estimate(sys_vect)
print("Returned estimate = f(" + str(received_est.x) + ") = " + str(received_est.fx))
print("Current estimate = f(" + str(a1.curr_est.x) + ") = " + str(a1.curr_est.fx))
print("Future estimate = f(" + str(a1.hist_med.x) + ") = " + str(a1.hist_med.fx))

x_vals = []
fx_vals = []
for b in range(len(a1.history)):
    x_vals.append(a1.history[b].x)
    fx_vals.append(a1.history[b].fx)
plt.scatter(x_vals,fx_vals)
plt.xlabel("Historical x value")
plt.ylabel("Historical f(x) value")
plt.show()
