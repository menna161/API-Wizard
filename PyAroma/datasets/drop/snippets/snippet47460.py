import re
from glob import glob
import numpy as np
import pandas as pd
import paper_reviewer_matcher as pm
import scipy.sparse as sp
from paper_reviewer_matcher import preprocess, compute_affinity, create_lp_matrix, create_assignment, linprog
from fuzzywuzzy import fuzz


def create_assignment_dataframe(b, reviewer_map, paper_id_map, pool_group='a'):
    '\n    Get the assignment array, generate assignment dataframe\n    '
    assignments = []
    for i in range(len(b)):
        assignments.append([paper_id_map[i], [reviewer_map[b_] for b_ in np.nonzero(b[i])[0]]])
    assignments_df = pd.DataFrame(assignments, columns=['PaperID', 'UserIDs'])
    n_reviewers = len(assignments_df.UserIDs.iloc[0])
    for c in range(n_reviewers):
        assignments_df['UserID_{}_{}'.format(pool_group, (c + 1))] = assignments_df.UserIDs.map((lambda x: x[c]))
    return assignments_df.drop('UserIDs', axis=1)
