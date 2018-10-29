from multiprocessing import Pool
import time

def square(x):  
    # calculate the square of the value of x
    return x*x

if __name__ == '__main__':
    
    t_start = time.clock()
    
    # Define the dataset
    dataset = range(10000000)

    # Output the dataset
   # print ('Dataset: ' + str(dataset))

    # Run this with a pool of 5 agents having a chunksize of 3 until finished
    agents = 2
    pool = Pool(processes=agents)
    result = pool.map(square, dataset)

    # Output the result
   # print ('Result:  ' + str(result))
    
    print(time.clock() - t_start)