import numpy as np
from numpy.linalg import inv, norm
import matplotlib.pyplot as plt


def solve_lambda_x(A, y, lambs_exponent=np.arange((- 10), 5, 0.01)):
    '\n    Minimize the Lagrangian L(x,lambda) = || A*x - y||**2 + lambda*||x||**2 based on the idea of Tikhonov Regularization.\n    This program is used to roughly estimate the parameters x and the Lagrange multiplier lambda. \n    The L-curve method is applied to get the proper Lagrangian multiplier.\n\n    Usage:\n    estimate_lamb,estimate_x,log10_residual_norm,log10_solution_norm,curvature = solve_lambda_x(A,y) \n\n    Inputs:\n    A -> [float 2d array] Design matrix\n    y -> [float array] Measurements\n\n    Parameters:\n    lambs_exponent -> [optional, float 3d/4d array, default = np.arange(-10,5,0.01)] Exponent for lambda with base of 10\n    \n    Outputs:\n    estimate_lamb -> [float] Lagrange multiplier\n    estimate_x -> [float array] Estimated parameters\n    log10_residual_norm -> [float array] log10(||A*x-y||) with lambda taking 10**lambs_exponent\n    log10_solution_norm -> [float array] log10(||x||) with lambda taking 10**lambs_exponent\n    curvature -> [float array] curvature of the L-curve, where the ordinate of the curve is log10_solution_norm and the abscissa is log10_residual_norm.\n\n    For more information, please refer to \n    (1) [NumPy/SciPy Recipes for Data Science: Regularized Least Squares Optimization](https://www.researchgate.net/publication/274138835_NumPy_SciPy_Recipes_for_Data_Science_Regularized_Least_Squares_Optimization)\n    (2) [Choosing the Regularization Parameter](http://www2.compute.dtu.dk/~pcha/DIP/chap5.pdf)\n    '
    np.seterr(divide='ignore', invalid='ignore')
    m = A.shape[1]
    (log10_residual_norm, log10_solution_norm) = ([], [])
    lambs = np.float_power(10, lambs_exponent)
    for lamb in lambs:
        x = np.dot(inv((np.dot(A.T, A) + (lamb * np.eye(m)))), np.dot(A.T, y))
        residual_norm = norm((np.dot(A, x) - y))
        solution_norm = norm(x)
        log10_residual_norm.append(np.log10(residual_norm))
        log10_solution_norm.append(np.log10(solution_norm))
    log10_residual_norm = np.array(log10_residual_norm)
    log10_solution_norm = np.array(log10_solution_norm)
    g1 = np.gradient(log10_solution_norm, log10_residual_norm)
    g1[np.isnan(g1)] = (- np.inf)
    g2 = np.gradient(g1, log10_residual_norm)
    g2[np.isnan(g2)] = np.inf
    curvature = (np.abs(g2) / ((1 + (g1 ** 2)) ** 1.5))
    curvature[np.isnan(curvature)] = 0
    curvature[np.isinf(curvature)] = 0
    index_curvature_max = np.argmax(curvature)
    estimate_lamb = lambs[index_curvature_max]
    estimate_x = np.dot(inv((np.dot(A.T, A) + (estimate_lamb * np.eye(m)))), np.dot(A.T, y))
    return (estimate_lamb, estimate_x, log10_residual_norm, log10_solution_norm, curvature)
