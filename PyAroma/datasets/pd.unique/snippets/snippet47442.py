import numpy as np
import pandas as pd
from paper_reviewer_matcher import preprocess, compute_affinity, create_lp_matrix, linprog, create_assignment
import random
import networkx as nx
import fastcluster
import scipy.cluster.hierarchy as hierarchy
from fuzzywuzzy import fuzz


def convert_names_to_ids(names, person_id_map, threshold=85):
    "\n    Convert string of names with separated comma to list of IDs using fuzzy string match\n\n    Parameters\n    ==========\n    names: str, string in the following format 'FirstName1 LastName1, ...'\n    person_id_map: dict, dictionary mapping id to name\n\n    Example\n    =======\n    >> convert_names_to_ids('Jone Doe, Sarah Doe', \n                            {1: 'Jone Doe', 2: 'Sarah Deo'}, threshold=85) # output [1, 2]\n    "
    from fuzzywuzzy import fuzz
    matched_ids = []
    names = [name.strip() for name in names.split(',')]
    for name in names:
        matched_ids.extend([idx for (idx, n) in person_id_map.items() if (fuzz.ratio(n, name) >= threshold)])
    return pd.unique(matched_ids)
