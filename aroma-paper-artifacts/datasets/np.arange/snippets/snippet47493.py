import numpy as np
import pandas as pd
from fuzzywuzzy import fuzz
from tqdm.auto import tqdm
from .lp import linprog
from .affinity import create_lp_matrix, create_assignment


def perform_mindmatch(A: np.array, n_trim: int=None, n_match: int=6, cois: list=None):
    '\n    Perform mindmatching with a given matrix A,\n    trimming of n_trim (reduce problem size),\n    matching between n_match people\n    '
    A[(np.arange(len(A)), np.arange(len(A)))] = (- 1000)
    cois = [(c1, c2) for (c1, c2) in cois if ((c1 <= len(A)) and (c2 <= len(A)))]
    A[np.array(cois)] = (- 1000)
    if (n_trim != 0):
        A_trim = []
        for r in range(len(A)):
            a = A[(r, :)]
            a[np.argsort(a)[0:n_trim]] = 0
            A_trim.append(a)
        A_trim = np.vstack(A_trim)
    else:
        A_trim = A
    print('Solving a matching problem...')
    (v, K, d) = create_lp_matrix(A_trim, min_reviewers_per_paper=n_match, max_reviewers_per_paper=n_match, min_papers_per_reviewer=n_match, max_papers_per_reviewer=n_match)
    x_sol = linprog(v, K, d)['x']
    b = create_assignment(x_sol, A_trim)
    if (b.sum() == 0):
        print('Seems like the problem does not converge, try reducing <n_trim> but not too low!')
    else:
        print('Successfully assigned all the match!')
    return b
