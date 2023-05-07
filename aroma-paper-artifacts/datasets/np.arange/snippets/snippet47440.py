import numpy as np
import pandas as pd
from paper_reviewer_matcher import preprocess, compute_affinity, create_lp_matrix, linprog, create_assignment
import random
import networkx as nx
import fastcluster
import scipy.cluster.hierarchy as hierarchy
from fuzzywuzzy import fuzz


def create_dating_schedule(person_df, n_meeting=10):
    '\n    Function to create speed dating schedule at CCN 2018 conference\n\n    Parameters\n    ==========\n    person_df: pandas dataframe contains - PersonID, FullName, Abstract\n    n_meeting: int, number of meeting we would like to have\n\n    Output\n    ======\n    schedule: list, list of person id and person ids to meet in the \n        following format: [PersonID, [PersonID to meet]]\n    '
    persons_1 = list(map(preprocess, list(person_df['Abstract'])))
    persons_2 = list(map(preprocess, list(person_df['Abstract'])))
    A = compute_affinity(persons_1, persons_2, n_components=10, min_df=1, max_df=0.8, weighting='tfidf', projection='pca')
    A[(np.arange(len(A)), np.arange(len(A)))] = (- 1000)
    (v, K, d) = create_lp_matrix(A, min_reviewers_per_paper=n_meeting, max_reviewers_per_paper=n_meeting, min_papers_per_reviewer=n_meeting, max_papers_per_reviewer=n_meeting)
    x_sol = linprog(v, K, d)['x']
    b = create_assignment(x_sol, A)
    output = []
    for i in range(len(b)):
        r = [list(person_df['PersonID'])[b_] for b_ in np.nonzero(b[i])[0]]
        output.append([list(person_df.PersonID)[i], r])
    schedule = nest_answer(output, format_answer(color_graph(build_line_graph(output))))
    return schedule
