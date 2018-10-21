# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-10-10
@name: model_agent.py

-------------------------------------------------------------------------------
Description:
    
This file contains a model of an agent in a the system. It contains the def-
inition of the class agent including its properties. Those properties include a
selection of an objective function, definition of a current estimate,
definition of a historical median as a future projection estimate, and the
position of the agent in the system network. Both inputs are optional, and may
be specified as follows below.

Parameters:
    
    est_type_prob = [0,1]
        A value on the continuous domain from 0 to 1 which specifies the
        probability that an agent will generate estimates corresponding to
        a future design. Therefore, a value of 0 corresponds to 100% current
        designs and a value of 1 corresponds to 100% future designs.
    obj_fn = (string)
        A string input which specifies the objective function the agent uses
        to evaluate the quality of a design. The input must be one of the
        following terms, specified with quotes:
            "sphere"          - uses the sphere function as the objective,
                                which is also the default setting
            "ackley"          - uses the Ackley function as the objective
            "rosenbrock"      - uses the Rosenbrock function as the objective
            "styblinski-tang" - uses the Styblinski-Tang function as objective

-------------------------------------------------------------------------------
Change Log:

Date:       Author:    Description:
2018-10-10  jmeluso    Initial version.
-------------------------------------------------------------------------------
"""

# Import python packages
import numpy as np
from numpy import exp, cos, pi, sqrt, vdot
from scipy.optimize import basinhopping as min_fn


class Agent(object):
    '''Defines a class agent which designs an artifact in a system.'''


    def __init__(self, loc, nbr, est_type_prob=0.5, obj_fn="sphere"):
        '''Initializes an agent with all of its properties.'''

        ##### Network Properties #####
        
        self.location = loc  # Define the agent index in the system
        self.neighbors = nbr  # Define a vector of the agent's neighbors

        ##### Objective Properties #####

        self.fn = obj_fn  # Specify the evaluating objective function

        # Set decision variable boundaries
        if self.fn == "ackley":
            self.obj_bounds = Bounds(-32.768,32.768)
        elif self.fn == "rosenbrock":
            self.obj_bounds = Bounds(-5.00,10.00)
        elif self.fn == "styblinski-tang":
            self.obj_bounds = Bounds(-5.00,5.00)
        else:  # self.fn == "sphere" or none
            self.obj_bounds = Bounds(-5.12,5.12)

        ##### Estimate Properties #####
        
        self.curr_est = Obj_Eval()  # Initialize the agent's current estimate
        self.history = []  # First row x's, second row f(x)'s
        self.hist_med = Obj_Eval()  # Initialize the agent's historical median

        # Determine the type of estimate being used by the agent. If greater
        # than estimate probability...
        if (np.random.random_sample() > est_type_prob):
            self.est_type = "current"  # Set estimate type as current design
        else:  # Else less than or equal to the estimate probability
            self.est_type = "future"  # Set estimate type as future projection


    def __repr__(self):
        '''Returns a representation of the agent'''
        return self.__class__.__name__
    
    
    def set_system_locations(self,location,neighbors):
        '''Takes a location and vector of neighbors from the system and uses
        those values to populate the agent's own fields.'''
        
        # Set the agent's location and specify its neighbors
        self.location = location
        self.neighbors = neighbors
        
    def initialize_estimates(self):
        '''Uses the history generated so far to set the historical median and
        generates a random value for the initial current estimate.'''
        
        # Find the median historical value
        inputs = []
        outputs = []
        for h in self.history:
            inputs.append(h.x)
            outputs.append(h.fx)
        
        median_index = np.argsort(outputs)[len(outputs)//2]
        self.hist_med.set_eval(inputs[median_index], outputs[median_index])
        
        # Initialize the agent's current estimate by randomly generating an
        # a value on the domain of the objective function inputs
        # (-bound,+bound)
        self.curr_est.x = ((self.obj_bounds.xmax - self.obj_bounds.xmin)* \
                           np.random.random_sample() + self.obj_bounds.xmin)


    def generate_history(self,sys_vect):
        '''Uses a system vector only to generate one historical value for the
        agent. The agent evaluates the inputs using its objective function.
        Then, the agent compiles the generated decision variable value and
        objective evaluation.'''
        
        xi = sys_vect[self.location]
        xj = []  # Initialize a vector of neighbors' values

        # Extract neighbors' values from system vector
        for j in self.neighbors:
            xj.append(sys_vect[j])

        # Create a new evaluation from inputs
        result = self.objective(xi,xj)

        # Save x and f(x) as an objective evaluation to the history list
        self.history.append(Obj_Eval(xi,result))


    def generate_estimate(self,sys_vect):
        '''Uses a system vector input and the current agent estimate to
        generate one estimate value for the agent. The agent then compiles the
        generated decision variable value and objective evaluation. Finally,
        the agent uses its estimate type to determine which value (the current
        or future) of the estimate to return.'''
        
        xi = self.curr_est.x
        xj = []  # Initialize a vector of neighbors' values
        
        # Extract neighbors' values from system vector
        for j in self.neighbors:
            xj.append(sys_vect[j])

        # Create a new estimate by optimizing with inputs and own values
        estimate = self.optimize(xi,xj)

        # Save results
        self.curr_est.x = estimate.x[0]
        self.curr_est.fx = estimate.fun

        # Return an estimate ("current" or "future")
        if self.est_type == "current":
            return self.curr_est.x  # Return current value to system
        else:  # self.est_type == "future"
            # Return the lesser of the historical median and current value
            if self.curr_est.fx < self.hist_med.fx:
                # The current estimate is better, so return it
                return self.curr_est.x
            else:
                # Return historical median to system
                return self.hist_med.x


    def optimize(self,xi,xj):
        '''Optimizes the agent's design using the objective function and inputs
        from neighbor agents. Minimize is the scipy.optimize.basinhopping
        method which supercedes the simulated annealing algorithm in python.
        The function takes in the agent's own value (xi) and the neighbors
        vector (xj).'''

        # Call the minimization method
        result =  min_fn(func = self.objective,
                         x0 = xi,
                         niter = 1,
                         stepsize = (self.obj_bounds.xmax \
                                     - self.obj_bounds.xmin)/10,
                         minimizer_kwargs = {"args": xj,"method": "BFGS"},
                         accept_test = self.obj_bounds)
        
        # Return the result
        return result


    def objective(self,xi,xj):
        '''Based on the agent's own input (xi), a selected function (fn), and
        the inputs of the other agents (a vector, xj, of length k), this method
        calculates the specified objective function evaluation and returns the
        solution. '''

        # Calculate the node's degree from neighbor vector length
        k = len(xj)

        # Select the correct function to evaluate
        if self.fn == "ackley":

            # Set values of constants for ackley function
            a = 20
            b = 0.2
            c = 2*pi

            # Build the sums for function evaluation
            cos_sum = 0
            for j in xj:
                cos_sum = cos_sum + cos(c*j)

            # Evaluate the ackley function
            root_term = -a*exp(-b*sqrt((xi**2 + vdot(xj,xj))/(k + 1)))
            cos_term = -exp((cos(c*xi) + cos_sum)/(k + 1))

            # Return the function evaluation
            result = root_term + cos_term + a + exp(1)
        
        elif self.fn == "styblinski-tang":
            
            # Build the sums for function evaluation
            xi_term = xi**4 - 16*xi**2 + 5*xi
            xj_term = 0
            for j in xj:
                xj_term = xj_term + j**4 - 16*j**2 + 5*j
                
            # Return the outcome
            result = 0.5*(xi_term + xj_term)
            
        elif self.fn == "rosenbrock":
            
            # Build vector of all elements
            vect = xj
            vect.insert(0,xi)
            
            # Build double sum
            result = 0
            for i in range(1,len(vect)-1):
                result = result + (100*(vect[i+1]-vect[i]**2)**2
                                   + (vect[i]-1)**2)

        else:

            # Evaluate the sphere function
            result = xi**2 + vdot(xj,xj)

        # Return the outcome
        return result


class Obj_Eval(object):
    '''Defines a class Obj_Eval for function evaluation which has two values,
    an input x and an output f(x) which represent one of several types of
    objective evaluations.'''
    
    def __init__(self,x=[],fx=[]):
        '''Initializes an instance of a function evaluation with all of its
        properties.'''
        
        self.x = x  # Initialize the input value of the function
        self.fx = fx  # Initialize the output value of the function


    def __repr__(self):
        '''Returns a representation of the function evaluation.'''
        return self.__class__.__name__
    
    
    def get_eval(self):
        '''Gets the values stored in the function eval class.'''
        
        return [self.x,self.fx]  # Return the objective evaluation pair
    
    
    def set_eval(self,x=[],fx=[]):
        '''Updates the values saved in the function evaluation object.'''
        
        if x != []: # If the update value isn't empty
            self.x = x  # Update x
        if fx != []: # If the update value isn't empty
            self.fx = fx  # Update fx

        
class Bounds(object):
    '''Defines a set of bounds, upper and lower, within which to evaluate an
    objective function.'''
    
    def __init__(self,xmin,xmax):
        '''Initializes the bounds class with min and max values.'''
        self.xmin = xmin
        self.xmax = xmax
    
    def __call__(self, **kwargs):
        '''Checks to see if a value falls within the specified bounds or not
        and returns either True or False accordingly.'''
        x = kwargs["x_new"]
        tmin = bool(np.all(x >= self.xmin))
        tmax = bool(np.all(x <= self.xmax))
        return tmin and tmax
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    
    