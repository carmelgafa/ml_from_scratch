
import os
import matplotlib
matplotlib.rcParams['text.usetex'] = True
import matplotlib.pyplot as plt
import pandas as pd
import sys
import numpy as np

def LinearRegression(a, cd, batch_size):

    file = 'data.csv'
    
    alpha = a
    threshold_iterations = 100000
    costdifference_threshold = cd

    # load the training data
    full_filename = os.path.join(os.path.dirname(__file__), file)
    training_data = pd.read_csv(full_filename, delimiter=',', header=0, index_col=False)

    # training_data = training_data.sample(frac=1).reset_index(drop=True)

    # divide the data into features and labels
    X = training_data.drop(['y'], axis=1).to_numpy()
    # add a column of ones to the features matrix to account for the intercept, a0
    X = np.insert(X, 0, 1, axis=1)

    Y = training_data['y'].to_numpy()
    
    # length of the training data
    m = len(Y)

    # initialize the y_hat vector to 0
    y_hat = np.zeros(len(Y))
    
    # beta will hold the values of the coefficients, hence it will be  the size 
    # of a row of the X matrix
    # initialize beta to random values
    beta = np.random.random(len(X[0]))

    # minibatches setting
    # number of minibatches = m => stochastic gradient descent
    # number of minibatches = 1 => batch gradient descent
    minibatches_number = batch_size
    minibatch_size = int(m/minibatches_number)

    # initialize the number of epochs
    epochs = 0

    # initialize the previous cost function value to a large number
    # previous_cost = sys.float_info.max
    
    # store the cost function and a2 values for plotting
    costs = []
    a_2s = []
    
    previous_cumulative_cost = sys.float_info.max
    
    # loop until exit condition is met
    while True:

        cumulative_cost = 0

        for i in range(minibatches_number):

            # print(f'Minibatch: {i}')
            minibatch_X = X[i*minibatch_size:(i+1)*minibatch_size]
            minibatch_Y = Y[i*minibatch_size:(i+1)*minibatch_size]

            # calculate the hypothesis function for all training data
            y_hat = np.dot(beta, minibatch_X.T)

            #  calculate the residuals
            residuals = y_hat - minibatch_Y

            # calculate the new value of beta
            beta -= (
                alpha / minibatch_size)  * np.dot(
                    residuals, minibatch_X)

            # calculate the cost function
            cost = np.dot(residuals, residuals) / ( 2 * minibatch_size)

            cumulative_cost += cost

        # increase the number of iterations
        epochs += 1

        # record the cost and a1 values for plotting
        #     costs.append(cost)
        #     a_2s.append(__beta[2])

        cost_difference = previous_cumulative_cost - cumulative_cost
        # print(f'Epoch: {epochs}, average cost: {(cumulative_cost/minibatches_number):.3f}, beta: {beta}')
        previous_cumulative_cost = cumulative_cost

        # check if the cost function is diverging, if so, break
        # if cost_difference < 0:
        #     print(f'Cost function is diverging. Stopping training.')
        #     break
            
        # check if the cost function is close enough to 0, if so, break or if the number of 
        # iterations is greater than the threshold, break
        if abs(cost_difference) < costdifference_threshold or epochs > threshold_iterations:
            break

    # # plot the cost function and a1 values
    # plt.plot(a_2s[3:], costs[3:], '--bx', color='lightblue', mec='red')
    # plt.xlabel('a2')
    # plt.ylabel('cost')
    # plt.title(r'Cost Function vs. a1, with $\alpha$ =' + str(__alpha))
    # plt.show()
    
    # calculate the cost for the training data and return the beta values and 
    # the number of iterations and the cost
    y_hat = np.dot(beta, X.T)
    residuals = y_hat - Y
    cost = np.dot(residuals, residuals) / ( 2 * m)
    
    return beta, epochs, cost
    

if __name__ == '__main__':

    from timeit import default_timer as timer

    start = timer()
    print(LinearRegression(0.0023, 0.0001, 1))
    end = timer()
    print(f'Time: {end - start}')
    
    start = timer()
    print(LinearRegression(0.0015, 0.001, 2))
    end = timer()
    print(f'Time: {end - start}')
    
    start = timer()
    print(LinearRegression(0.0010, 0.001, 20))
    end = timer()
    print(f'Time: {end - start}')

    start = timer()
    print(LinearRegression(0.001, 0.001, 200))
    end = timer()
    print(f'Time: {end - start}')
    
    start = timer()
    print(LinearRegression(0.001, 0.001, 1000))
    end = timer()
    print(f'Time: {end - start}')