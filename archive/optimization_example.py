# -*- coding: utf-8 -*-
"""
Created on Thu Oct 25 15:53:55 2018

@author: Juango the Blue
"""

import numpy as np
from numpy import pi, cos, sqrt, exp, dot
import scipy.optimize as opt

###############################################################################

# List of objective functions available
obj_fn = ["ackley","styblinski-tang","rosenbrock","sphere"]
num_fn = len(obj_fn)

# Set fn bounds
obj_bounds = [[-32.768,32.768],
              [-5.00,10.00],
              [-5.00,5.00],
              [-5.12,5.12]]

# Set the max degree
k_max = 1000

# Create extrema matrices
min_by_degree = np.empty([num_fn,k_max])
max_by_degree = np.empty([num_fn,k_max])

# Optimize to find extrema
for k in range(k_max):
    for fn in obj_fn:
        
        # Optimize 




###############################################################################

def objective(fn,x):
    '''Uses a function input and an x vector to evaluate the function.'''

    # Calculate the node's degree from neighbor vector length
    d = len(x)

    # Select the correct function to evaluate
    if fn == "ackley":

        # Set values of constants for ackley function
        a = 20
        b = 0.2
        c = 2*pi

        # Build the sums for function evaluation
        cos_sum = 0
        for j in x:
            cos_sum = cos_sum + cos(c*j)

        # Return the function evaluation
        result = -a*exp(-b*sqrt((dot(x,x))/d) - exp(cos_sum/d) + a + exp(1)
    
    elif fn == "styblinski-tang":
        
        # Build the sum for function evaluation
        for j in x:
            x_term = x_term + j**4 - 16*j**2 + 5*j
            
        # Return the outcome
        result = 0.5*x_term
        
    elif fn == "rosenbrock":
        
        # Call scipy function for rosenbrock
        result = opt.rosen(x)

    else:

        # Evaluate the sphere function
        result = dot(x,x)

    # Return the outcome
    return result

def optimize(self,xi,xj):
    '''Optimizes the agent's design using the objective function and inputs
    from neighbor agents. The function takes in the agent's own value (xi)
    and the neighbors vector (xj). It selects the appropriate optimization
    algorithm for the function.'''
    
    # Use basinhopping only for multiple-minimum functions
    if self.fn == "ackley":

        # Call the basin hopping minimization method
        output = opt.basinhopping(func = self.objective,
                         x0 = xi,,
                         minimizer_kwargs = {"args": xj},
                         accept_test = self.obj_bounds)
        
        # Save the desired outputs in float format
        if isinstance(output.fun,np.ndarray):
            result = Obj_Eval(output.x[0],output.fun[0])
        else:
            result = Obj_Eval(output.x[0],output.fun)
        
    else:  # Use gradient for single- or few-minimum functions
        
        # Call the bounded brent scalar minimization function
        output = opt.minimize_scalar(fun = self.objective,
                         bounds = (self.obj_bounds.xmin,\
                                   self.obj_bounds.xmax),
                         args = (xj),
                         method = 'bounded')
        
        # Save the desired outputs
        result = Obj_Eval(output.x,output.fun)
    
    # Return the result
    return result