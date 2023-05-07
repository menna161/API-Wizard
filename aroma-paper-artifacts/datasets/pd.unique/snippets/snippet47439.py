import numpy as np
import pandas as pd
from paper_reviewer_matcher import preprocess, compute_affinity, create_lp_matrix, linprog, create_assignment
import random
import networkx as nx
import fastcluster
import scipy.cluster.hierarchy as hierarchy
from fuzzywuzzy import fuzz


def schedule_to_timeslot(schedule, n_timeslot=15):
    '\n    Create personal schedule from list of schedule\n    '
    schedule_df = pd.DataFrame(schedule, columns=['person', 'person_to_meet'])
    person_to_meet_df = pd.DataFrame(schedule_df.person_to_meet.values.tolist(), columns=range(1, n_timeslot))
    schedule_df = pd.concat((schedule_df[['person']], person_to_meet_df), axis=1)
    person_list = pd.unique(list(schedule_df['person']))
    P_map = {v: k for (k, v) in enumerate(person_list)}
    timeslot_list = []
    for i in range(1, n_timeslot):
        timeslot_df = schedule_df[['person', i]].dropna().astype(int).reset_index(drop=True)
        P = np.zeros((len(person_list), len(person_list)), dtype=int)
        count = 1
        for (_, r) in schedule_df.iterrows():
            if ((not pd.isnull(r['person'])) and (not pd.isnull(r[i])) and (P[(P_map[r['person']], P_map[r[i]])] == 0) and (P[(P_map[r[i]], P_map[r['person']])] == 0)):
                P[(P_map[r['person']], P_map[r[i]])] = count
                P[(P_map[r[i]], P_map[r['person']])] = count
                count += 1
        left_person = list((set(person_list) - set(pd.unique((list(timeslot_df.person) + list(timeslot_df[i].dropna().astype(int)))))))
        random.shuffle(left_person)
        random_pair = list(zip(left_person[0:int((len(left_person) / 2))], left_person[int((len(left_person) / 2)):]))
        for (p1, p2) in random_pair:
            count += 1
            P[(P_map[p1], P_map[p2])] = count
            P[(P_map[p2], P_map[p1])] = count
        additional_pair = ([[p1, p2, int(P[(P_map[p1], P_map[p2])])] for (p1, p2) in random_pair] + [[p2, p1, int(P[(P_map[p1], P_map[p2])])] for (p1, p2) in random_pair])
        left_person_df = pd.DataFrame(additional_pair, columns=['person', i, 'table_number'])
        table_number = [int(P[(P_map[r['person']], P_map[r[i]])]) for (_, r) in timeslot_df.iterrows()]
        timeslot_df['table_number'] = table_number
        timeslot_df = pd.concat((timeslot_df, left_person_df))
        timeslot_list.append(timeslot_df)
    person_schedule_all = []
    for p in person_list:
        person_schedule = []
        for t_df in timeslot_list:
            person_schedule.append(t_df[(t_df.person == p)])
        person_schedule_all.append(pd.concat(person_schedule))
    return person_schedule_all
