import numpy as np


def mean_and_cov_matrix(data):
    # Returns and covriance matrix
    M = []
    C = []

    for key1, value1 in data.items():
        Return = np.mean(value1)/value1[0] - 1
        M.append(Return)

        CL = []
        for key2, value2 in data.items():
            cov = value1.cov(value2)
            CL.append(cov)
        C.append(CL)
        
    M = np.array(M)
    C = np.array(C)

    return  M, C
