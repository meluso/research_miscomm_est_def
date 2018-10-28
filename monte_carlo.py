# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-10-10
@name: monte_carlo.py

Performs a Monte Carlo simulation on a network of engineer agents. This
model initializes and runs an instance of the system model, and sweeps the
probability that an agent will use a specific estimate type. The model executes
1000 times for each parameter combination using full factorial sampling.

"""
import model_system as sy
import multiprocessing as mp
    
###############################################################################
# Initialize simulation parameters
###############################################################################
    
# Number of trials to perform for each permutation of variables
num_trials = 1

# Number of agents in the model
num_agents = 1000

# A list of the different objective functions available to the agents.
obj_fn = [
        "sphere", 
        #"ackley", 
        #"rosenbrock", 
        #"styblinski-tang"
        ]
num_fn = len(obj_fn)

# A list of values to sample for probability of estimate types
est_prob = [float(i)/10 for i in range(11)]
num_prob = len(est_prob)

# A list of the different estimation methods used for historical data
est_meth = ["future_est", "best_est"]
num_meth = len(est_meth)


###############################################################################
# Simulation Storage & Logistics
###############################################################################

# Array corresponding to all of the variables of the trial
sim_stor = []
pool = mp.Pool(processes=2)


###############################################################################
# Run Simulation
###############################################################################

# Loop through each of the parameters and store the results
for fn in range(num_fn):
    for pr in range(num_prob):
        for mt in range(num_meth):
            for tr in range(num_trials):
                
                # Build unique run ID
                run_ID = str(mt + 1) + "." \
                    + str(fn + 1) + "." \
                    + str(pr + 1).zfill(2) + "." \
                    + str(tr + 1).zfill(5)
                
                # Initialize the system
                model = sy.System(num_agents,
                                  obj_fn[fn],
                                  est_prob[pr],
                                  est_meth[mt])
                
                # Run the simulation
                output = model.run()
                
                # Store the results in the array
                sim_stor.append([
                        run_ID,
                        est_meth[mt],
                        obj_fn[fn],
                        est_prob[pr],
                        output.design_cycles,
                        output.perf_system[-1],
                        output.k_mean,
                        output.perf_agents,
                        output.k_agents
                        ])
                
                print("Completed: fn " + str(fn + 1) + "/" + str(num_fn)
                      + ", prob " + str(pr + 1) + "/" + str(num_prob)
                      + ", meth " + str(mt + 1) + "/" + str(num_meth)
                      + ", trial " + str(tr + 1) + "/" + str(num_trials) + ".")







                
###############################################################################
# Execution Function
###############################################################################                
                    
                
                
def execute_trial(num_agents,mt,fn,pr,tr):
    '''Executes a single trial of the Monte Carlo simulation. Function creates
     an instances of a system, runs the model for that system, and saves the
     results of the trial.'''
     
                
                
                
                
                