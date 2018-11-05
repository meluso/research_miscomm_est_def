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
import doe_lhs as doe

class System(object):
    '''Defines a class system which contains a specified number of agents that
    are engineers designing various components. Also includes methods for
    advancing the system from an initial to a final converged design.'''

    def __init__(self, n = 1000, obj = "sphere", p = 0.5, mthd = ""):
        '''Initializes an instance of the system model.'''
        
        ##### Agent Properties #####
        self.obj_fn = obj  # The objective function used by the agents
        self.mthd = mthd  # Initialize the type of future estimates being made
        
        ##### Network Properties #####
        
        self.n = n  # The number of agents in the network
        self.new_edges = 2  # The number of edges created with each new node
        self.p = p  # The probability of a new edge creating a triangle
        
        # Generate the network using generate_network
        self.system = self.generate_network()
        
        ##### System Properties #####
        
        self.s = 101  # The number of hypercube sampling partitions
        self.conv_lim = 1  # System convergence limit
        
        # Vector (old and new) of the agents' returned values
        self.vect = [ag.Obj_Eval() for i in range(n)]
        self.vect_new = [ag.Obj_Eval() for i in range(n)]
        
        # Generate the system history        
        self.generate_history()
        
        for i in range(len(self.system)):
            
            # Initialize the agent's estimate
            self.system[i].initialize_estimates()
        
            # Return the estimates to the system
            self.vect_new[i] = self.system[i].get_estimate()
        
        # Create a vector of just estimates for evaluation initialization
        est_vect = [self.vect_new[i].x for i in range(self.n)]
        
        for i in range(len(self.system)):
            
            # Populate the initial function evaluations of the agents
            self.system[i].initialize_evaluations(est_vect)
            
            # Return the estimates to the system
            self.vect_new[i] = self.system[i].get_estimate()
            
        # Transfer new values to system as current system design
        self.vect = self.vect_new

    
    def __repr__(self):
        '''Returns a representation of the agent'''
        return self.__class__.__name__
    

    def generate_network(self):
        '''Creates a system with nodes drawn from a scale-free degree
        distribution and creates an agent for each node.'''
        
        # Use networkx to create a network of the specified number of nodes
        self.graph = gen(self.n,self.new_edges,self.p)
        
        # Create an empty system
        system = []
        
        # Attach an agent of class model_agent to each node
        for i in self.graph:
            
            # Get a list of all the neighbors of node i
            nbrs = np.sort([j for j in self.graph.adj[i]])
            
            # Create agent in system with specified inputs for its neighbors,
            # probability of estimate type, and objective function
            system.append(ag.Agent(i,nbrs,self.p,self.obj_fn,self.mthd))
            
        # Return the generated network of agents
        return system


    def generate_history(self):
        '''Creates a historical profile for all of the agents through Latin
        Hypercube sampling all of the agents a specified number of times.'''
        
        # Generate a latin hypercube sampling for the agents
        samples = 101  # Set number of samples to take
        
        # Create the hypercube sample
        self.hypercube = doe.lhs(self.n,samples)
        
        # Scale the hypercube samples to the agents' bounds
        for i in range(len(self.system)):
            
            # Get bounds from agent
            min_val = self.system[i].obj_bounds.xmin
            max_val = self.system[i].obj_bounds.xmax
            
            # Scale all of the agents' samples to that range
            for h in range(samples):
                self.hypercube[h][i] = min_val + (max_val - min_val)* \
                                       self.hypercube[h][i]
        
        # Cycle through all of the hypercube sample vectors
        for h in range(samples):
            
            # Give the agents initial points to run one optimization on
            for i in range(len(self.system)):
                self.vect_new[i] = \
                    self.system[i].rand_hist_init(self.hypercube[h])
            
            # Give agents the optimized vector to evaluate and save
            for a in self.system:
                a.save_history(self.vect_new)
    
    
    def design_cycle(self):
        '''Perform a single design cycle with all of the agents.'''
        
        # For each agent
        for i in range(len(self.system)):
            
            # Perform one design cycle with current system vector
            self.vect_new[i] = self.system[i].generate_estimate(self.vect)
            
        # Record all system design values returned by agents
        self.vect = self.vect_new
            
    
    def run(self):
        '''Designs the system. Assumes the system has already been initialized
        with histories for each agent.'''
        
        # Initialize design cycle counter and convergence flag
        dc = 0
        cv = 0
        
        # Create performance vector and sum
        perf_vect = [self.vect[i].fx for i in range(self.n)]
        perf_sys = []
        perf_sys.append(sum(perf_vect))
        
        # Perform design cycles until converged
        while (cv == 0) and (dc < 100):
            
            # Increment design cycle counter
            dc = dc + 1
            
            # Perform a design cycle by calling design_cycle
            self.design_cycle()
            
            # Evaluate the system's performance
            perf_vect = [self.vect[i].fx for i in range(self.n)]
            perf_sys.append(sum(perf_vect))
            
            # Check convergence conditions
            if dc > 3:
                
                # Check current evaluation against current-3
                if abs(perf_sys[-1] - perf_sys[-1 - 3]) < self.conv_lim:
                    cv = 1 # Set the convergence flag to terminate
                
            else:
                
                # Check current evaluation against the original evaluation
                if abs(perf_sys[-1] - perf_sys[0]) < self.conv_lim:
                    cv = 1 # Set the convergence flag to terminate
                    
            
            
        # Collect all of the information from this system to return after the
        # run of the simulation. It returns the following information: the
        # number of design cycles required for convergence, the system
        # performance at the end of the design cycles, the mean degree of the
        # network, the final performance of each agent, and the degree of each
        # agent.
        
        k_agents = [d for n, d in self.graph.degree()] # Get the agents' degrees
        k_mean = np.mean(k_agents)
        perf_ag = [[i.x,i.fx] for i in self.vect]
        
        # Build the results vector
        results = Results(dc, perf_sys, k_mean, perf_ag, k_agents)
        
        # Return the results
        return results


class Results(object):
    '''An object which returns a specified set of properties from the system
    after completion of a simulation run.'''
    
    def __init__(self, des_cyc, perf_system, k_mean, perf_agents, k_agents):
        '''Creates an instances of the results object to return the outputs of
        the simulation to the monte carlo.'''
    
        self.design_cycles = des_cyc
        self.perf_system = perf_system
        self.k_mean = k_mean
        self.perf_agents = perf_agents
        self.k_agents = k_agents