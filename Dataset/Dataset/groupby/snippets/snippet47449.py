import itertools
import numpy as np
import pandas as pd
import random
import networkx as nx
from itertools import chain
from fuzzywuzzy import fuzz
from paper_reviewer_matcher import preprocess, compute_affinity, create_lp_matrix, linprog, create_assignment
from docx import Document


def create_coi_dataframe(df, people_maps, threshold=85, coreferred=True):
    '\n    For a given dataframe of for mind-match people with \n    ``full_name``, ``mindMatchExcludeList`` column, and \n    a dictionary that map ``full_name`` to person_id, \n    create conflict of interest dataframe\n\n    Parameters\n    ==========\n    df: dataframe, original mind matching dataset\n    people_maps: list, list dictionary that map person id to their person_id, full_name, and affiliation\n    threshold: int, fuzzy string match ratio for matching name in ``mindMatchExcludeList`` and ``full_name``\n    coreferred: bool, if True, add extra conflict of interest for people who mentioned the same person\n\n    Output\n    ======\n    coi_df: dataframe, conflict of interest\n    '
    coi_list = []
    for (i, r) in df.iterrows():
        if (len(r['mindMatchExcludeList']) > 0):
            exclude_list = []
            for exclude in r['mindMatchExcludeList']:
                exclude_list.extend([p['person_id'] for p in people_maps if ((exclude in p['full_name']) or (fuzz.ratio(p['full_name'], exclude) >= threshold) or (fuzz.ratio(p['affiliation'], exclude) >= threshold))])
            exclude_list = sorted(pd.unique(exclude_list))
            if (len(exclude_list) > 0):
                for e in exclude_list:
                    coi_list.append([i, e])
    coi_df = pd.DataFrame(coi_list, columns=['person_id', 'person_id_exclude'])
    if coreferred:
        coi_coreferred = [[g, list(g_df.person_id)] for (g, g_df) in coi_df.groupby(['person_id_exclude']) if (len(list(g_df.person_id)) >= 2)]
        coi_coreferred_list = []
        for (_, exclude_list) in coi_coreferred:
            coi_coreferred_list.extend(list(itertools.combinations(exclude_list, 2)))
        coi_coreferred_df = pd.DataFrame(coi_coreferred_list, columns=['person_id', 'person_id_exclude'])
        coi_df = pd.concat((coi_df, coi_coreferred_df))
        return coi_df
    else:
        return coi_df
