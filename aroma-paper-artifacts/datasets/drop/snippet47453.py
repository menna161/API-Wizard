from glob import glob
import numpy as np
import pandas as pd
import scipy.sparse as sp
from paper_reviewer_matcher import preprocess, compute_affinity, create_lp_matrix, linprog, create_assignment


def assign_articles_to_reviewers(article_df, reviewer_df, people_df):
    '\n    Perform reviewer-assignment from dataframe of article, reviewer, and people\n\n    Parameters\n    ==========\n    article_df: a dataframe that has columns `PaperID`, `Title`, `Abstract`, and `PersonIDList`\n        where PersonIDList contains string of simicolon separated list of PersonID\n    reviewer_df: a dataframe that has columns `PersonID` and `Abstract`\n    people_df:  dataframe that has columns `PersonID`, `FullName`\n\n    We assume `PersonID` is an integer\n\n    Output\n    ======\n    article_assignment_df: an assigned reviewers dataframe, each row of article will have \n        list of reviewers in `ReviewerIDList` column and their name in reviewer_names\n    '
    papers = list(((article_df['Title'] + ' ') + article_df['Abstract']).map(preprocess))
    reviewers = list(reviewer_df['Abstract'].map(preprocess))
    coauthors_df = pd.DataFrame([[int(r.PaperID), int(co_author)] for (_, r) in article_df.iterrows() for co_author in r.PersonIDList.split(';')], columns=['PaperID', 'PersonID'])
    article_df['paper_id'] = list(range(len(article_df)))
    reviewer_df['person_id'] = list(range(len(reviewer_df)))
    coi_df = coauthors_df.merge(article_df[['PaperID', 'paper_id']], on='PaperID').merge(reviewer_df[['PersonID', 'person_id']], on='PersonID')[['paper_id', 'person_id']]
    A = compute_affinity(papers, reviewers, n_components=10, min_df=2, max_df=0.8, weighting='tfidf', projection='pca')
    A_trim = []
    for r in range(len(A)):
        a = A[(r, :)]
        a[np.argsort(a)[0:200]] = 0
        A_trim.append(a)
    A_trim = np.vstack(A_trim)
    for (i, j) in zip(coi_df.paper_id.tolist(), coi_df.person_id.tolist()):
        A_trim[(i, j)] = (- 1000)
    (v, K, d) = create_lp_matrix(A_trim, min_reviewers_per_paper=6, max_reviewers_per_paper=6, min_papers_per_reviewer=4, max_papers_per_reviewer=6)
    x_sol = linprog(v, K, d)['x']
    b = create_assignment(x_sol, A_trim)
    reviewer_ids = list(reviewer_df.PersonID)
    reviewer_name_dict = {r['PersonID']: r['FullName'] for (_, r) in people_df.iterrows()}
    assignments = []
    for i in range(len(b)):
        assignments.append([i, [reviewer_ids[b_] for b_ in np.nonzero(b[i])[0]], [reviewer_name_dict[reviewer_ids[b_]] for b_ in np.nonzero(b[i])[0]]])
    assignments_df = pd.DataFrame(assignments, columns=['paper_id', 'ReviewerIDList', 'reviewer_names'])
    assignments_df['ReviewerIDList'] = assignments_df.ReviewerIDList.map((lambda e: ';'.join((str(e_) for e_ in e))))
    assignments_df['reviewer_names'] = assignments_df.reviewer_names.map((lambda x: ';'.join(x)))
    article_assignment_df = article_df.merge(assignments_df, on='paper_id').drop('paper_id', axis=1)
    return article_assignment_df
