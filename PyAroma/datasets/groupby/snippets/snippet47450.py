import itertools
import numpy as np
import pandas as pd
import random
import networkx as nx
from itertools import chain
from fuzzywuzzy import fuzz
from paper_reviewer_matcher import preprocess, compute_affinity, create_lp_matrix, linprog, create_assignment
from docx import Document


def convert_mind_match_to_document(mind_matching_df, table_map=None, file_name='ccn_mindmatch_2019.docx'):
    '\n    Create full schedule for mind matching into word document format,\n    printing person name, affiliation, registration id, and list of person to meet\n    '
    pages = []
    for (person_id, mind_matching_schedule_df) in mind_matching_df.groupby('person_id'):
        page = []
        page.extend([person_id_map[person_id], person_affil_map[person_id], 'RegID: {}'.format(registration_id_map[person_id])])
        page.extend(['----------------------', 'Mind Matching Schedule', '----------------------'])
        for (_, r) in mind_matching_schedule_df.iterrows():
            if (table_map is not None):
                table_number = table_map[r['table_number']]
            else:
                table_number = r['table_number']
            page.extend(['timeslot: {}, table number: {}, mind-match: {} ({})'.format(r['timeslot'], table_number, person_id_map[r['person_to_meet_id']], person_affil_map[r['person_to_meet_id']])])
        pages.append('\n'.join(page))
    document = Document()
    for page in pages:
        document.add_paragraph(page)
        document.add_page_break()
    document.save(file_name)
