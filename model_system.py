# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-10-10
@name: model_system.py

This file contains a model of networked miscommunication in a system. It creates
the system network, the agents assigned to each node in the network, the
history of each agent in the network, and the process of designing the system.

"""

# Import python packages
from networkx.generators.random_graphs import powerlaw_cluster_graph as gen
import numpy as np
import model_agent as ag

class System(object):
    '''Defines a class system which contains a specified number of agents that
    are engineers designing various components. Also includes methods for
    advancing the system from an initial to a final converged design.'''

    def __init__(self, n = 1000, m = 2, p = 0.5):
        '''Initializes an instance of the system model.'''
        
        ##### Agent Properties #####
        self.obj_fn = "sphere"  # The objective function used by the agents
        
        ##### Network Properties #####
        
        self.n = n  # The number of agents in the network
        self.m = m  # The number of edges created with each new node
        self.p = p  # The probability of a new edge creating a triangle
        
        # Generate the network using generate_network
        self.system = self.generate_network()
        
        ##### System Properties #####
        
            # Get initial system design vector from agents
            # Initialize final system design vector variable
            # Define system convergence limit
            # Generate system histories using generate_history

    
    def __repr__(self):
        '''Returns a representation of the agent'''
        return self.__class__.__name__
    

    def generate_network(self):
        '''Creates a system with nodes drawn from a scale-free degree
        distribution and creates an agent for each node.'''
        
        # Use networkx to create a network of the specified number of nodes
        self.graph = gen(self.n,self.m,self.p)
        
        # Create an empty system
        system = []
        
        # Attach an agent of class model_agent to each node
        for i in self.graph:
            
            # Get a list of all the neighbors of node i
            nbrs = np.sort([j for j in self.graph.adj[i]])
            
            # Create agent in system with specified inputs for its neighbors,
            # probability of estimate type, and objective function
            system.append(ag.Agent(i,nbrs,self.p,self.obj_fn))
            
        # Return the generated network of agents
        return system
    
    
    def run(self):
        '''Designs the system. Assumes the system has already been initialized
        with histories for each agent.'''
        
        # While system design has not converged and
        # the system has not reached max number of design cycles
            # Perform a design cycle by calling design_cycle
            # Increment design cycle counter

    
    def generate_history(self):
        '''Creates a historical profile for all of the agents through Latin
        Hypercube sampling all of the agents a specified number of times.'''
        
        # Generate specified number of random sampling combination vectors which
            # determine where in the design domain of each agent the decision
            # variable for each agent will be drawn from. For example,
            # partition each of 3 agents' design spaces into 5 values. Then
            # vectors [2,5,3], [3,4,1], [5,2,4], [1,3,2], and [4,1,5] form an
            # unbiased sample of the design space.
        
        # For each sampling combination
            # For each agent
                # Feed the agent the system design vector
                # Ask agent to store its input value and objective evaluation
                
        # For each agent
            # Set each agent's history profile
    
    
    def design_cycle(self):
        '''Perform a single design cycle with all of the agents.'''
        
        # For each agent
            # Give agent initial system design vector    
            # Perform one design cycle
            # Record final system design value returned by agent
            