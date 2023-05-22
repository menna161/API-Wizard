import numpy as np
import pandas as pd
from paper_reviewer_matcher import preprocess, compute_affinity, create_lp_matrix, linprog, create_assignment
import random
import networkx as nx
import fastcluster
import scipy.cluster.hierarchy as hierarchy
from fuzzywuzzy import fuzz

if (__name__ == '__main__'):
    '\n    Example script to create dating schedule for CCN 2018 conference\n    '
    person_df = pd.ExcelFile('CCN18_MindMatchData.xlsx').parse('Grid Results')
    person_df['FullName'] = ((person_df['NameFirst'] + ' ') + person_df['NameLast'])
    person_df['PersonID'] = np.arange(len(person_df))
    person_id_map = {r['PersonID']: r['FullName'] for (_, r) in person_df.iterrows()}
    person_affil_map = {r['PersonID']: r['Affiliation'] for (_, r) in person_df.iterrows()}
    schedule = create_dating_schedule(person_df)
    n_timeslot = (len(schedule[0][(- 1)]) + 1)
    person_schedule_all = schedule_to_timeslot(schedule, n_timeslot=n_timeslot)
    n_meeting = 6
    output_text = []
    for person_schedule_df in person_schedule_all:
        output_text.extend(['You are: ', str(person_id_map[person_schedule_df.person.unique()[0]])])
        output_text.extend(['--------------------'])
        output_text.extend(['Dating schedule'])
        output_text.extend(['--------------------'])
        r = 0
        for i in range(1, (n_meeting + 1)):
            person_to_meet = [l for l in list(person_schedule_df[i]) if (not pd.isnull(l))]
            if (len(person_to_meet) > 0):
                table_number = person_schedule_df['table_number'].iloc[r]
                output_text.extend([('timeslot: %d, table number: %d, date: %s' % (i, table_number, person_id_map[person_to_meet[0]]))])
                r += 1
            else:
                output_text.extend([('timeslot: %d, Waiting area!' % i)])
        output_text.extend([''])
    with open('output_date_schedule.txt', 'w') as f:
        for l in output_text:
            f.write('{}\n'.format(l))
