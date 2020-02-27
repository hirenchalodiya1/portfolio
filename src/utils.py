import numpy as np
import cvxpy as cp
import pandas as pd


def mean_and_cov_matrix(data):
    # Returns and covriance matrix
    M = []
    C = []

    for key, value in data.items():
        ret_matrix = []
        zero_value = value[0]
        for val in value:
            ret_matrix.append((val-zero_value)/zero_value)
        data[key] = pd.Series(ret_matrix)

    for key1, value1 in data.items():
        Return = np.mean(value1)
        M.append(Return)

        CL = []
        for key2, value2 in data.items():
            cov = value1.cov(value2)
            CL.append(cov)
        C.append(CL)
        
    M = np.array(M)
    C = np.array(C)
    print(M)
    print(C)
    return  M, C


def solvePortfolio(cov_matrix, mean_matrix, expected_mean=None):
    n = len(mean_matrix)
    w = cp.Variable(n)
    risk = cp.quad_form(w, cov_matrix)
    conditions = [
        sum(w) == 1,
        mean_matrix @ w.T == expected_mean
    ]
    if expected_mean is None:
        conditions = [
            sum(w) == 1
        ]
    
    prob = cp.Problem(cp.Minimize(risk), conditions)
    prob.solve()
    return w.value
