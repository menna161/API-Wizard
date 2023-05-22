import pandas as pd
import config
from sklearn.model_selection import train_test_split
import numpy as np
import os


def main():
    df_train = pd.read_csv(config.RAW_TRAIN_DATA, sep='\t', names=['a1', 'a2', 'e1', 'e2', 'r', 's'], na_values=[], keep_default_na=False)
    df_test = pd.read_csv(config.RAW_TEST_DATA, sep='\t', names=['a1', 'a2', 'e1', 'e2', 'r', 's', 'end'], na_values=[], keep_default_na=False)
    df_train = df_train[['a1', 'r', 'a2']]
    df_test = df_test[['a1', 'r', 'a2']]
    df_all = pd.concat([df_train, df_test], ignore_index=True)
    df_all.r = df_all.r.map(transform)
    df_fb = pd.read_csv(config.KB, sep='\t', names=['a1', 'r', 'a2'])
    dSet = set((list(df_all.a1) + list(df_all.a2)))
    f = open(config.E2ID, 'w')
    for (i, e) in enumerate(dSet):
        f.write(('%s %d\n' % (e, i)))
    f.close()
    fSet = set((list(df_fb.a1) + list(df_fb.a2)))
    print(('%d entities in data' % len(dSet)))
    print(('%d entities in subgraph of freebase' % len(fSet)))
    print(('%d entities in both' % len(dSet.intersection(fSet))))
    print(('=' * 50))

    def triples(x):
        return (x.a1, x.r, x.a2)
    mask = df_all.r.map((lambda x: (x != 'NA')))
    df_test.r = df_test.r.map(transform)
    mask = df_test.r.map((lambda x: (x != 'NA')))
    tFact = set(list(df_test[mask].apply(triples, axis=1)))
    fFact = set(list(df_fb.apply(triples, axis=1)))
    print(('%d facts in test data' % len(tFact)))
    print(('%d facts in subgraph of freebase' % len(fFact)))
    assert (len(tFact.intersection(fFact)) == 0), 'Testing facts exist in subgraph!!!'
    print(('%d facts in both' % len(tFact.intersection(fFact))))
    print(('=' * 50))

    def check(x):
        return ((x.a1, x.r, x.a2) not in tFact)
    print('Constructing KG for embedding training...')
    n = df_fb.shape[0]
    X = np.zeros((n, 2))
    y = np.arange(n)
    (_, _, train_idx, valid_idx) = train_test_split(X, y, test_size=10000)
    df_train = df_fb.iloc[train_idx]
    df_valid = df_fb.iloc[valid_idx]
    df_test = df_valid.iloc[:10]
    print(('Saving to %s' % config.KG_PATH))
    if (not os.path.exists(config.KG_PATH)):
        os.makedirs(config.KG_PATH)
    df_train.to_csv((config.KG_PATH + '/train.txt'), sep='\t', header=False, index=False)
    df_valid.to_csv((config.KG_PATH + '/valid.txt'), sep='\t', header=False, index=False)
    df_test.to_csv((config.KG_PATH + '/test.txt'), sep='\t', header=False, index=False)
