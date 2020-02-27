import numpy as np
import cvxpy as cp


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
