import itertools
import numpy as np
import pandas as pd
import random
import networkx as nx
from itertools import chain
from fuzzywuzzy import fuzz
from paper_reviewer_matcher import preprocess, compute_affinity, create_lp_matrix, linprog, create_assignment
from docx import Document

if (__name__ == '__main__'):
    df = pd.read_csv('CN19_MindMatchData_20190903-A.csv', encoding='iso-8859-1')
    df['full_name'] = ((df['NameFirst'] + ' ') + df['NameLast'])
    df['person_id'] = list(range(len(df)))
    people_maps = [{'person_id': r['person_id'], 'full_name': r['full_name'], 'affiliation': r['Affiliation']} for (i, r) in df.iterrows()]
    person_id_map = {r['person_id']: r['full_name'] for (_, r) in df.iterrows()}
    person_affil_map = {r['person_id']: r['Affiliation'] for (_, r) in df.iterrows()}
    registration_id_map = {r['person_id']: r['RegistrantID'] for (_, r) in df.iterrows()}
    if ('mindMatchExclude' in df.columns):
        df['mindMatchExcludeList'] = df.mindMatchExclude.fillna(',').map(split_exclude_string)
        coi_df = create_coi_dataframe(df, people_maps, threshold=85, coreferred=True)
    n_meeting = 6
    persons_1 = list(map(preprocess, list(df['RepresentativeWork'])))
    persons_2 = list(map(preprocess, list(df['RepresentativeWork'])))
    A = compute_affinity(persons_1, persons_2, n_components=10, min_df=2, max_df=0.8, weighting='tfidf', projection='pca')
    A[(np.arange(len(A)), np.arange(len(A)))] = (- 1000)
    for (_, r) in coi_df.iterrows():
        A[(r['person_id'], r['person_id_exclude'])] = (- 1000)
        A[(r['person_id_exclude'], r['person_id'])] = (- 1000)
    n_trim = 2
    A_trim = []
    for r in range(len(A)):
        a = A[(r, :)]
        a[np.argsort(a)[0:n_trim]] = 0
        A_trim.append(a)
    A_trim = np.vstack(A_trim)
    print('Solving linear programming for Mind-Matching session...')
    (v, K, d) = create_lp_matrix(A_trim, min_reviewers_per_paper=6, max_reviewers_per_paper=6, min_papers_per_reviewer=6, max_papers_per_reviewer=6)
    x_sol = linprog(v, K, d)['x']
    b = create_assignment(x_sol, A_trim)
    print('Done!')
    output = []
    for i in range(len(b)):
        r = [list(df['person_id'])[b_] for b_ in np.nonzero(b[i])[0]]
        output.append([list(df.person_id)[i], r])
    schedule = nest_answer(output, format_answer(color_graph(build_line_graph(output))))
    schedule_df = pd.DataFrame(schedule, columns=['person_id', 'match_id'])
    schedule_df['match_id'] = schedule_df.match_id.map((lambda x: x[0:n_meeting]))
    mind_matching_df = []
    for i in range(n_meeting):
        schedule_df['match'] = schedule_df.match_id.map((lambda x: x[i]))
        match_pairs = list(pd.unique([frozenset((r['person_id'], int(r['match']))) for (_, r) in schedule_df.iterrows() if (not pd.isnull(r['match']))]))
        r = list((set(schedule_df.person_id) - set(schedule_df['match'].dropna().unique().astype(int))))
        random.shuffle(r)
        match_pairs.extend(list(map(frozenset, zip(r[0:int((len(r) / 2))], r[int((len(r) / 2)):]))))
        match_lookup = [(list(k), v) for (v, k) in enumerate(match_pairs, start=1)]
        person_lookup = {}
        for (k, v) in match_lookup:
            person_lookup[k[0]] = k[1]
            person_lookup[k[1]] = k[0]
        match_df = pd.DataFrame(list(chain.from_iterable([[[k[0], v], [k[1], v]] for (k, v) in match_lookup])), columns=['person_id', 'table_number'])
        match_df['person_to_meet_id'] = match_df.person_id.map((lambda x: person_lookup[x]))
        match_df['timeslot'] = (i + 1)
        mind_matching_df.append(match_df)
    mind_matching_df = pd.concat(mind_matching_df)
    table_map = {k: v for (k, v) in enumerate([(str(i) + c) for i in range(1, 33) for c in 'abcd'], start=1)}
    convert_mind_match_to_document(mind_matching_df, table_map, file_name='ccn_mindmatch_2019.docx')
    convert_mind_match_to_minimized_format(mind_matching_df, table_map, file_name='ccn_mindmatch_2019_minimized.csv')
    print('Saved matched files into CSV and DOCX format.')
