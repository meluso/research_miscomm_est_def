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
a1 = ag.Agent(2,[0,3],0.5,"styblinski-tang","best_est")
print("Location = " + str(a1.location))
print("Neighbors = " + str(a1.neighbors))
print("Bound = " + str(a1.obj_bounds.xmax))
print("Estimate type = " + str(a1.est_type))
print("Objective function type = " + a1.fn)

# Create a history vector for a set of 4 agents
sys_vect = [ag.Obj_Eval() for i in range(4)]
for h in range(0,101):
    lhs_vect = [rand(),rand(),rand(),rand()]
    sys_vect[2] = a1.rand_hist_init(lhs_vect)
    est_vect = [ag.Obj_Eval(rand(),rand()),
                ag.Obj_Eval(rand(),rand()),
                sys_vect[2],
                ag.Obj_Eval(rand(),rand())]
    for i in range(4):
        a1.save_history(est_vect)
        
print("History = " + str(len(a1.history)) + " points")

# Set initial estimates for the agent
a1.initialize_estimates()
print("--Initial estimate--")
print("Current estimate = " + str(a1.curr_est.x))
print("Future estimate = " + str(a1.hist_med.x))

# Create an estimate
sys_vect = [ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand())]
received_est = a1.generate_estimate(sys_vect)
print("--1st updated estimate--")
print("Returned estimate = " + str(received_est.x))
print("Current estimate = " + str(a1.curr_est.x))
print("Future estimate = " + str(a1.hist_med.x))

# Create an estimate
sys_vect = [ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand()),
            ag.Obj_Eval(rand(),rand())]
received_est = a1.generate_estimate(sys_vect)
print("--2nd updated estimate--")
print("Returned estimate = " + str(received_est.x))
print("Current estimate = " + str(a1.curr_est.x))
print("Future estimate = " + str(a1.hist_med.x))