import numpy as np
import pandas as pd
from docopt import docopt
from paper_reviewer_matcher import preprocess, compute_topics, perform_mindmatch, compute_conflicts, calculate_affinity_distance
from sklearn.cluster import SpectralClustering

if (__name__ == '__main__'):
    arguments = docopt(__doc__, version='MindMatch 0.1.dev')
    file_name = arguments['PATH']
    df = pd.read_csv(file_name).fillna('')
    assert ('user_id' in df.columns), 'CSV file must have ``user_id`` in the columns'
    assert ('fullname' in df.columns), 'CSV file must have ``fullname`` in the columns'
    assert ('abstracts' in df.columns), 'CSV file must have ``abstracts`` in the columns'
    assert ('conflicts' in df.columns), 'CSV file must have ``conflicts`` in the columns'
    print('Number of people in the file = {}'.format(len(df)))
    n_match = arguments.get('--n_match')
    if (n_match is None):
        n_match = 6
        print('<n_match> is set to default for 6 match per user')
    else:
        n_match = int(n_match)
        print('Number of match is set to {}'.format(n_match))
    assert (n_match >= 2), 'You should set <n_match> to be more than 2'
    n_trim = arguments.get('--n_trim')
    if (n_trim is None):
        n_trim = 0
        print('<n_trim> is set to default, this will take very long to converge for a large problem')
    else:
        n_trim = int(n_trim)
        print('Trimming parameter is set to {}'.format(n_trim))
    n_clusters = arguments.get('--n_clusters')
    if (n_clusters is None):
        n_cluters = 4
        print('Setting number of clusters <n_cluters> to 4')
    else:
        n_clusters = int(n_clusters)
        print('Setting number of clusters to 4')
    output_filename = arguments.get('output')
    if (output_filename is None):
        output_filename = 'output_match.csv'
    X_topic = compute_topics(list(map(preprocess, list(df['abstracts']))))
    spectral_clustering = SpectralClustering(n_clusters=n_clusters, random_state=42)
    labels = spectral_clustering.fit_predict(X_topic)
    labels[0] = 3
    df['group'] = labels
    df['topics'] = [x for x in X_topic]
    output = []
    for (_, df_group) in df.groupby('group'):
        X = np.vstack(df_group.topics.values)
        A = calculate_affinity_distance(X, X)
        cois = compute_conflicts(df_group.reset_index(drop=True))
        b = perform_mindmatch(A, n_trim=10, n_match=6, cois=cois)
        user_ids_map = {ri: r['user_id'] for (ri, r) in df_group.reset_index(drop=True).iterrows()}
        for i in range(len(b)):
            match_ids = [str(user_ids_map[b_]) for b_ in np.nonzero(b[i])[0]]
            output.append({'user_id': user_ids_map[i], 'match_ids': ';'.join(match_ids)})
    output_df = pd.DataFrame(output)
    output_df.to_csv(output_filename, index=False)
