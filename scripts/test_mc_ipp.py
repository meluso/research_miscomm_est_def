# -*- coding: utf-8 -*-
"""
@author: John Meluso
@date: 2018-11-04
@name: test_mc_test.py

Performs a Monte Carlo simulation on a network of engineer agents. This
model initializes and runs an instance of the system model, and sweeps the
probability that an agent will use a specific estimate type. The model executes
1000 times for each parameter combination using full factorial sampling.

"""
import model_system as sy
import ipyparallel as ipp
import datetime as dt
import csv

###############################################################################
# Execution Function
###############################################################################                

def execute_trial(x):
    '''Executes a single trial of the Monte Carlo simulation. Function creates
     an instances of a system, runs the model for that system, and saves the
     results of the trial.'''
         
    # Convert x to model input values
    run_ID = x[0]
    num_agents = x[1]
    obj_fn = x[2]
    est_prob = x[3]
    est_meth = x[4]
    
    # Initialize the system
    model = sy.System(num_agents, obj_fn, est_prob, est_meth)
    
    # Run the simulation
    output = model.run()
    
    # Store the results in the array
    results_summary = [
            run_ID,
            est_meth,
            obj_fn,
            est_prob,
            output.design_cycles,
            output.perf_system[-1],
            output.k_mean
            ]
    
    results_system = output.perf_system
    
    results_agents = [output.perf_agents,output.k_agents]
    
    # Return results
    return [results_summary, results_system, results_agents]

    
###############################################################################
# Initialize simulation parameters
###############################################################################
    
if __name__ == '__main__':
    
    # Start timer
    t_start = dt.datetime.now()
    
    # Number of trials to perform for each permutation of variables
    num_trials = 1
    
    # Number of agents in the model
    num_agents = 10
    
    # A list of the different objective functions available to the agents.
    obj_fn = [
            "sphere", 
            "ackley", 
            "rosenbrock", 
            "styblinski-tang"
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
    sim_inputs = []
    results_summary = []
    results_system = []
    results_agents = []

###############################################################################
# Run Simulation
###############################################################################

    # Loop through each of the parameters to create an input matrix
    for fn in range(num_fn):
        for pr in range(num_prob):
            for mt in range(num_meth):
                for tr in range(num_trials):
                    
                    # Build unique run ID
                    run_ID = str(mt + 1) + "." \
                        + str(fn + 1) + "." \
                        + str(pr + 1).zfill(2) + "." \
                        + str(tr + 1).zfill(5)
                    
                    # Populate the simulation inputs array
                    sim_inputs.append([run_ID,
                            num_agents,
                            obj_fn[fn],
                            est_prob[pr],
                            est_meth[mt]])
    
    # Run simulation through pool of workers with sim_inputs
    print(sim_inputs)
    sim_outputs = pool.map(execute_trial,sim_inputs)
    pool.close()
    pool.join()


###############################################################################
# Save Results to File
###############################################################################
    
    # Parse the results into matrices
    for i in range(len(sim_outputs)):
        results_summary.append(sim_outputs[i][0])
        results_system.append(sim_outputs[i][1])
        results_agents.append(sim_outputs[i][2])

    # Write the results to a CSV file stamped with the time
    filename = dt.datetime.now().isoformat()[0:20].replace("T","_").\
        replace(":","-").replace(".","_")
    
    # Construct a file for the summary
    with open("../results/"+filename+"MCResultsSummary.csv","wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in results_summary:
            writer.writerow(line)
            
    # Construct a file for the system results
    with open("../results/"+filename+"MCResultsSystem.csv","wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in results_system:
            writer.writerow(line)
            
    # Construct a file for the 
    with open("../results/"+filename+"MCResultsAgents.csv","wb") as csv_file:
        writer = csv.writer(csv_file, delimiter=',')
        for line in results_agents:
            writer.writerow(line)

    # Stop timer
    t_stop = dt.datetime.now()
    print(t_stop - t_start)

                
                
                
                