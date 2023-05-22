import hashlib
import json
import logging
import os
import urllib
import zipfile
from collections import namedtuple
from pathlib import Path
import numpy as np
import pandas as pd
from rdflib import Graph
import requests


def _load_xai_fb15k_237_experiment_log(full=False, subset='all'):
    'Load the XAI FB15k-237 experiment log\n\n        XAI-FB15k-237 is a reduced version of FB15K-237 containing human-readable triples.\n\n        The dataset contains several fields, by default the returned data frame contains only triples, when\n        option full is equal to True (``full=True``) the full data is returned (it reflects filtering protocol).\n\n        Fields:\n\n        - predicate,\n        - predicate label,\n        - predicates_description,\n        - subject,\n        - subject_label,\n        - object_label,\n        - object.\n\n        All triples are returned 273 x 7.\n\n        Full Fields:\n\n        *note: some field can have 3 forms, these are marked with X, X = {1,2,3} for 3 triples,\n               that were displayed to the annotators with a given predicate.\n\n        - predicate: evaluated predicate,\n        - predicate label: human label for predicate,\n        - predicates_description: human description of what the predicate means,\n        - question triple X: textual form of triple 1 containing predicate,\n        - subject_tripleX: subject of triple X,\n        - object_tripleX: object of triple X,\n        - subject_label_tripleX: human label of subject of triple X,\n        - object_label_tripleX: human label of object of triple X,\n        - avg rank triple X: avergae rank that the triple obtain among models,\n        - std rank triple X: standard deviation of rank that the triple obtain among models,\n        - avg O rank triple X: average object rank that the triple obtain among models,\n        - std O rank triple X: standard deviation of object rank that the triple obtain among models,\n        - avg S rank triple X: average subject rank that the triple obtain among models,\n        - std S rank triple X: standard deviation of subject rank that the triple obtain among models,\n        - evaluated: summed score of 3 evaluators for a predicate (when each evaluator gave score 0 - not understandable or 1- understandable):\n                 0 - triples with this predicate are not understandable - full agreement between annotators.\n                 1 - triples with this predicate are mostly understandable - partial agreement between annotators.\n                 2 - triples with this predicate are mostly not understandable - partial agreement between annotators.\n                 3 - triples with this predicate are clearly understandable - full agreement between annotators.\n\n       All predicates are returned 91 x 37 records each containing 3 triples.\n\n        ============= ========= ==========\n        Dataset       Entities  Relations\n        ============= ========= ==========\n        XAI-FB15K-237  446       91\n        ============= ========= ==========\n\n\n        Parameters\n        ----------\n        full [False]: wether to return full dataset or reduced view with triples.\n        subset ["all"]: subset of records to be returned:\n             - "all" - returns all records,\n             - "clear" - returns only triples which all annotators marked as understandable,\n             - "not clear" - not understandable triples,\n             - "confusing+" - mostly understandable triples,\n             - "confusing-" - mostly not understandable.\n\n\n        X: pandas data frame containing triples (full=False), records with predicates (full=True).\n\n        Example\n        -------\n\n        >>> from ampligraph.datasets import _load_xai_fb15k_237_experiment_log\n        >>> X = _load_xai_fb15k_237_experiment_log()\n        >>> X.head(2)\n\n        predicate \t                        predicate label \tpredicates_description \t                        subject \tsubject_label \tobject_label \tobject\n    0 \t/media_common/netflix_genre/titles \tTitles \t                Titles that have this Genre in Netflix@en \t/m/07c52 \tTelevision \tFriends \t/m/030cx\n    1 \t/film/film/edited_by \t                Edited by \t        NaN \t                                        /m/0cc5qkt \tWar Horse \tMichael Kahn \t/m/03q8ch\n\n    '
    import requests
    url = 'https://ampgraphenc.s3-eu-west-1.amazonaws.com/datasets/xai_fb15k_237.csv'
    r = requests.get(url, allow_redirects=True)
    open('xai_fb15k_237.csv', 'wb').write(r.content)
    mapper = {'all': 'all', 'clear': 3, 'not clear': 0, 'confusing+': 2, 'confusing-': 1}
    if (subset != 'all'):
        if (subset in mapper):
            X = pd.read_csv('xai_fb15k_237.csv', sep=',')
            X = X[(X['evaluated'] == mapper[subset])]
        else:
            print('No such option!')
    else:
        X = pd.read_csv('xai_fb15k_237.csv', sep=',')
    if full:
        return X
    else:
        t1 = X[['predicate', 'predicate label', 'predicates_description', 'subject_triple1', 'subject_label_triple1', 'object_label_triple1', 'object_triple1']]
        t2 = X[['predicate', 'predicate label', 'predicates_description', 'subject_triple2', 'subject_label_triple2', 'object_label_triple2', 'object_triple2']]
        t3 = X[['predicate', 'predicate label', 'predicates_description', 'subject_triple3', 'subject_label_triple3', 'object_label_triple3', 'object_triple3']]
        mapper1 = {'subject_triple1': 'subject', 'subject_label_triple1': 'subject_label', 'object_label_triple1': 'object_label', 'object_triple1': 'object'}
        t1 = t1.rename(columns=mapper1)
        mapper2 = {'subject_triple2': 'subject', 'subject_label_triple2': 'subject_label', 'object_label_triple2': 'object_label', 'object_triple2': 'object'}
        t2 = t2.rename(columns=mapper2)
        mapper3 = {'subject_triple3': 'subject', 'subject_label_triple3': 'subject_label', 'object_label_triple3': 'object_label', 'object_triple3': 'object'}
        t3 = t3.rename(columns=mapper3)
        t1 = t1.append(t2, ignore_index=True)
        t1 = t1.append(t3, ignore_index=True)
        return t1
