import math
import numbers
import numpy as np
import scipy
from scipy.stats import norm


def gaussjordan(X, change=0):
    "Compute the binary row reduced echelon form of X.\n\n    Parameters\n    ----------\n    X: array (m, n)\n    change : boolean (default, False). If True returns the inverse transform\n\n    Returns\n    -------\n    if `change` == 'True':\n        A: array (m, n). row reduced form of X.\n        P: tranformations applied to the identity\n    else:\n        A: array (m, n). row reduced form of X.\n\n    "
    A = np.copy(X)
    (m, n) = A.shape
    if change:
        P = np.identity(m).astype(int)
    pivot_old = (- 1)
    for j in range(n):
        filtre_down = A[((pivot_old + 1):m, j)]
        pivot = ((np.argmax(filtre_down) + pivot_old) + 1)
        if A[(pivot, j)]:
            pivot_old += 1
            if (pivot_old != pivot):
                aux = np.copy(A[(pivot, :)])
                A[(pivot, :)] = A[(pivot_old, :)]
                A[(pivot_old, :)] = aux
                if change:
                    aux = np.copy(P[(pivot, :)])
                    P[(pivot, :)] = P[(pivot_old, :)]
                    P[(pivot_old, :)] = aux
            for i in range(m):
                if ((i != pivot_old) and A[(i, j)]):
                    if change:
                        P[(i, :)] = abs((P[(i, :)] - P[(pivot_old, :)]))
                    A[(i, :)] = abs((A[(i, :)] - A[(pivot_old, :)]))
        if (pivot_old == (m - 1)):
            break
    if change:
        return (A, P)
    return A
