import bisect
import logging
import random
import threading
import Stemmer
import numpy as np
import nltk
from sklearn.preprocessing import MinMaxScaler
from nltk.corpus import stopwords as stop_words
from scipy import sparse
from .utils import Indexer, create_sparse


def generate_samples(papers_observation_window, censoring_ratio, W, C):
    logging.info('generating samples ...')
    written_by = {}
    elements = sparse.find(W)
    for i in range(len(elements[0])):
        author = elements[0][i]
        paper = elements[1][i]
        if (paper in written_by):
            written_by[paper].append(author)
        else:
            written_by[paper] = [author]
    APPA = W.dot(C.dot(W.T))
    num_papers = W.dot(W.T).diagonal()
    observed_samples = {}
    for p in papers_observation_window:
        for u in p.authors:
            if (num_papers[u] >= paper_threshold):
                for paper_id in p.references:
                    if (paper_id in written_by):
                        for v in written_by[paper_id]:
                            if ((num_papers[v] >= paper_threshold) and (not APPA[(u, v)])):
                                if ((u, v) in observed_samples):
                                    observed_samples[(u, v)] = min(p.year, observed_samples[(u, v)])
                                else:
                                    observed_samples[(u, v)] = p.year
    nonzero = sparse.find(APPA)
    set_observed = set(([(u, v) for (u, v) in observed_samples] + [(u, v) for (u, v) in zip(nonzero[0], nonzero[1])]))
    censored_samples = {}
    N = APPA.shape[0]
    M = (len(observed_samples) // ((1 / censoring_ratio) - 1))
    author_list = [i for i in range(N) if (num_papers[i] >= paper_threshold)]
    while (len(censored_samples) < M):
        i = random.randint(0, (len(author_list) - 1))
        j = random.randint(0, (len(author_list) - 1))
        if (i != j):
            u = author_list[i]
            v = author_list[j]
            if ((u, v) not in set_observed):
                censored_samples[(u, v)] = (papers_observation_window[(- 1)].year + 1)
    return (observed_samples, censored_samples)
