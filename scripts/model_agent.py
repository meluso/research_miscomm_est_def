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
    
    loc = [0,1,...,n-2,n-1]
        An integer value from 0 to n-1 which specifies the location of the
        agent in the network of nodes. This and all other agents refer to the
        agent by this integer when referencing locations in the system.
    nbr = vect{[0,1,...,n-2,n-1]}
        A vector of integer values from 0 to n-1 which specifies the nodes in
        the network (by integer) which are neighbors of this agent.
    prob = [0,1]
        A value on the continuous domain from 0 to 1 which specifies the
        probability that an agent will generate estimates corresponding to
        a future design. Therefore, a value of 0 corresponds to 100% current
        designs and a value of 1 corresponds to 100% future designs.
    obj = (string)
        A string input which specifies the objective function the agent uses
        to evaluate the quality of a design. The input must be one of the
        following terms, specified with quotes:
            "sphere"          - uses the sphere function as the objective,
                                which is also the default setting
            "ackley"          - uses the Ackley function as the objective
            "rosenbrock"      - uses the Rosenbrock function as the objective
            "styblinski-tang" - uses the Styblinski-Tang function as objective
    mthd = (string)
        A string input which specifies which method of future projection
        estimates agents will make if they are specified as returning future
        estimates. The input must be one of the following terms, specified with
        quotes:
            "future_always"   - always returns the median of the historical
                                distribution as the estimate, even if the
                                current estimate is better
            "current_always"  - always returns the current estimate, even if
                                the historical median is better; provided in
                                case of potential issues with probabilities,
                                but unlikely necessary option
            "best_est"        - returns the better of the future estimate or
                                the current estimate depending on which of the
                                two estimates has a lower objective function
                                evaluation, where lower evaluations are better
            (none)            - the same as the best_est case

-------------------------------------------------------------------------------
Change Log:

Date:       Author:    Description:
2018-10-10  jmeluso    Initial version started.
2018-10-21  jmeluso    Initial version completed. Updates ongoing to tune the
                       model to perform in a way which produces meaningful
                       results.
2019-03-28  rojanov    Updated code for python3. 
-------------------------------------------------------------------------------
"""

# Import python packages
import numpy as np
from numpy import exp, cos, pi, sqrt, dot
import scipy.optimize as opt


class Agent(object):
    '''Defines a class agent which designs an artifact in a system.'''


    def __init__(self, loc, nbr, prob=0.5, obj="sphere", mthd = ""):
        '''Initializes an agent with all of its properties.'''

        ##### Network Properties #####
        
        self.location = loc  # Define the agent index in the system
        self.neighbors = nbr  # Define a vector of the agent's neighbors

        ##### Objective Properties #####

        self.fn = obj  # Specify the evaluating objective function
        
        # Create the agent's objective
        self.objective = Objective(self.fn,self.neighbors)

        # Set decision variable boundaries
        if self.fn == "ackley":
            #self.obj_bounds = Bounds(-32.768,32.768)
            self.obj_bounds = Bounds(-5.00,5.00)
        elif self.fn == "rosenbrock":
            self.obj_bounds = Bounds(-5.00,10.00)
        elif self.fn == "styblinski-tang":
            self.obj_bounds = Bounds(-5.00,5.00)
        else:  # self.fn == "sphere" or none
            self.obj_bounds = Bounds(-5.12,5.12)

        ##### Estimate Properties #####
        
        self.mthd = mthd  # Initialize the type of future estimates being made
        self.curr_est = Obj_Eval()  # Initialize the agent's current estimate
        self.history = []  # First row x's, second row f(x)'s
        self.hist_med = Obj_Eval()  # Initialize the agent's historical median

        # Determine the type of estimate being used by the agent. If greater
        # than estimate probability...
        if (np.random.random_sample() > prob):
            self.est_type = "current"  # Set estimate type as current design
        else:  # Else less than or equal to the estimate probability
            self.est_type = "future"  # Set estimate type as future projection


    def __repr__(self):
        '''Returns a representation of the agent'''
        return self.__class__.__name__
        
    
    def rand_hist_init(self,lhs_vect):
        '''Takes in a latin hypercube vector initialization to run a single
        design cycle. It then feeds this result back to the system without
        saving. This method is coupled with save history.'''
        
        xi = lhs_vect[self.location]
        
        # Initialize a vector of neighbors' values from Latin Hypercube Sample
        # vector (not an object Ojb_Eval)
        xj = [lhs_vect[j] for j in self.neighbors]

        # Optimize from the given inputs for one iteration
        result = self.optimize(xi,xj)
        
        # Return just the x from the optimized result
        return result
    
    
    def save_history(self,sys_vect):
        '''Saves a historical point by receiving corresponding optimized values
        from the other agents as it optimized its own variable. It then uses
        the objective function to evaluate the system vector. The x and f(x)
        of this evaluation are the saved historical point.'''
        
        xi = sys_vect[self.location].x
        
        # Initialize a vector of neighbors' values from the system vector
        # (which is an object Ojb_Eval)
        xj = [sys_vect[j].x for j in self.neighbors]
        
        # Evaluate the given inputs
        result = self.objective(xi, xj)
        
        # Save x and f(x) as an objective evaluation to the history list
        self.history.append(Obj_Eval(xi,result))
        
        
    def initialize_estimates(self):
        '''Uses the history generated so far to set the historical median and
        generates a random value for the initial current estimate.'''
        
        # Extract the input and output values from the agent's history.
        self.hist_in = [h.x for h in self.history]
        self.hist_out = [h.fx for h in self.history]
        
        # Initialize the agent's future estimate by using the historical
        # median's value.
        self.median_index = np.argsort(self.hist_out)[len(self.hist_out)//2]
        self.hist_med.x = self.hist_in[self.median_index]
        self.hist_med.fx = self.hist_out[self.median_index]
        
        # Initialize the agent's current estimate by randomly generating an
        # a value on the domain of the objective function inputs
        # (-bound,+bound)
        self.curr_est.x = ((self.obj_bounds.xmax - self.obj_bounds.xmin)* \
                           np.random.random_sample() + self.obj_bounds.xmin)
        
        
    def initialize_evaluations(self,sys_vect):
        '''Once all of the agents have been populated with their histories,
        they come up with an initial estiamte which they feed back to the
        system. Then, (as in this method) the system feeds the system vector
        back to the agents to populate the objective evaluations. Both the
        hist_med and curr_est function evaluations are performed here.'''
        
        # Get the historical median's objective evaluation
        self.hist_med.fx = self.hist_out[self.median_index]
        
        # Get own value for initial evaluation
        xi = self.curr_est.x
        
        # Initialize a vector of neighbors' values
        xj = [sys_vect[j] for j in self.neighbors]
        
        # Calculate the current estimate's objective evaluation
        self.curr_est.fx = self.objective(xi, xj)


    def get_estimate(self):
        '''Returns the appropriate estimate according to the type of estimate
        the agent is designated to return.'''
        
        # Return an estimate ("current" or "future")
        if self.est_type == "current":
            return self.curr_est  # Return current value to system
        else:  # self.est_type == "future"
            
            # Select return based on estimation method
            if self.mthd == "future_always":
                
                # Always return the future value
                return self.hist_med
            
            elif self.mthd == "current_always":
                
                # Always return the current value
                return self.curr_est
                
            else: # self.mthd == "best_est":
                
                # Only return the future value until the current is better.
                # Return the lesser of the historical median and current value.
                if self.curr_est.fx < self.hist_med.fx:
                    # The current estimate is better, so return it
                    return self.curr_est
                else:
                    # Return historical median to system
                    return self.hist_med


    def generate_estimate(self,sys_vect):
        '''Uses a system vector input and the current agent estimate to
        generate one estimate value for the agent. The agent then compiles the
        generated decision variable value and objective evaluation. Finally,
        the agent uses its estimate type to determine which value (the current
        or future) of the estimate to return.'''
        
        xi = self.curr_est.x
        
        # Initialize a vector of neighbors' values
        xj = [sys_vect[j].x for j in self.neighbors]

        # Create a new estimate by optimizing with inputs and own values
        estimate = self.optimize(xi,xj)

        # Save results
        self.curr_est.x = estimate.x
        self.curr_est.fx = estimate.fx
        
        # Return the estimate
        return self.get_estimate()


    def optimize(self,xi,xj):
        '''Optimizes the agent's design using the objective function and inputs
        from neighbor agents. The function takes in the agent's own value (xi)
        and the neighbors vector (xj). It selects the appropriate optimization
        algorithm for the function.'''
        
        # Use basinhopping only for multiple-minimum functions
        if self.fn == "ackley":
            
            # Define arguments for basin hopping minimization
            args = {"method": "L-BFGS-B",
                    "bounds": [(self.obj_bounds.xmin,self.obj_bounds.xmax)],
                    "args": xj}

            # Call the basin hopping minimization method
            output = opt.basinhopping(func = self.objective,
                             x0 = xi,
                             niter = 1,
                             stepsize = (self.obj_bounds.xmax \
                                         - self.obj_bounds.xmin)/10,
                             minimizer_kwargs = args,
                             accept_test = self.obj_bounds
                             )
            
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
                             args = xj,
                             method = 'bounded')
            
            # Save the desired outputs
            result = Obj_Eval(output.x,output.fun)
        
        # Return the result
        return result


class Objective:
    '''Based on the agent's own input (xi), a selected function (fn), and
    the inputs of the other agents (a vector, xj, of length k), this callable
    class calculates the specified objective function evaluation and returns
    the solution. '''
    
    def __init__(self,fn,neighbors):
        '''Initializes the objective function with the specified input function
        given by (fn) and calculates its degree (k) from its neighbors.'''
        
        self.fn = fn  # The selected objective function
        self.k = len(neighbors)  # The agent's degree
        

    def __call__(self,xi,xj):
        '''Executes the specified objective function with the inputs (xi) for
        the current agent and (xj) for the adjacent agents.'''        

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
            root_term = -a*exp(-b*sqrt((xi**2 + dot(xj,xj))/(self.k + 1)))
            cos_term = -exp((cos(c*xi) + cos_sum)/(self.k + 1))

            # Return the function evaluation
            result = root_term + cos_term + a + exp(1)
        
        elif self.fn == "styblinski-tang":
            
            # Build the sums for function evaluation
            xi_term = xi**4 - 16*xi**2 + 5*xi
            xj_term = 0
            for j in xj:
                xj_term = xj_term + j**4 - 16*j**2 + 5*j
                
            # Return the outcome
            result = 0.5*(xi_term + xj_term) + 39.166166*(self.k + 1)
            
        elif self.fn == "rosenbrock":
            
            # Build vector of all elements
            vect = xj
            vect.insert(0,xi)
            
            # Call scipy function for rosenbrock
            result = opt.rosen(vect)

        else:

            # Evaluate the sphere function
            result = xi**2 + dot(xj,xj)

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

        
class Bounds(object):
    '''Defines a set of bounds, upper and lower, within which to evaluate an
    objective function.'''
    
    def __init__(self,xmin,xmax):
        '''Initializes the bounds class with min and max values.'''
        self.xmax = np.array(xmax)
        self.xmin = np.array(xmin)
        
    def __call__(self, **kwargs):
        '''Checks to see if a value falls within the specified bounds or not
        and returns either True or False accordingly.'''
        x = kwargs["x_new"]
        tmax = bool(np.all(x <= self.xmax))
        tmin = bool(np.all(x >= self.xmin))
        return tmin and tmax