import itertools
import numpy as np
import pandas as pd
import random
import networkx as nx
from itertools import chain
from fuzzywuzzy import fuzz
from paper_reviewer_matcher import preprocess, compute_affinity, create_lp_matrix, linprog, create_assignment
from docx import Document


def convert_mind_match_to_minimized_format(mind_matching_df, table_map=None, file_name='ccn_mindmatch_2019_minimized.csv'):
    '\n    Convert full schedule for mind matching into CSV file with 2 columns\n    ``RegistrantID`` and ``ScheduleTables`` e.g. 1013, 1a|32a|1a|1a|1a|1a\n    '
    minimized_mind_matching = []
    for (person_id, mind_matching_schedule_df) in mind_matching_df.groupby('person_id'):
        if (table_map is not None):
            minimized_mind_matching.append({'RegistrantID': registration_id_map[person_id], 'ScheduleTables': '|'.join([table_map[e] for e in list(mind_matching_schedule_df.sort_values('timeslot').table_number.values)])})
        else:
            minimized_mind_matching.append({'RegistrantID': registration_id_map[person_id], 'ScheduleTables': '|'.join([e for e in list(mind_matching_schedule_df.sort_values('timeslot').table_number.values)])})
    minimized_mind_matching_df = pd.DataFrame(minimized_mind_matching)
    minimized_mind_matching_df.to_csv(file_name, index=False)
