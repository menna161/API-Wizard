import argparse
import numpy as np
import os
import random
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from joblib import dump
import multiprocessing as mp
from multiprocessing import Manager
import plasclass_utils as utils


def train(plasfile, chromfile, outdir, num_procs, ks=[3, 4, 5, 6, 7], lens=[1000, 10000, 100000, 500000]):
    ' Train PlasClass models\n    '
    print('Starting PlasClass training')
    print('Getting reference lengths')
    (chrom_names, chrom_lengths) = get_seq_lengths(chromfile)
    (plas_names, plas_lengths) = get_seq_lengths(plasfile)
    for l in lens:
        coverage = 5
        num_frags = get_num_frags(plas_lengths, l, coverage)
        print('Sampling {} fragments for length {}'.format(num_frags, l))
        plas_start_inds = get_start_inds(plas_names, plas_lengths, num_frags, l)
        chrom_start_inds = get_start_inds(chrom_names, chrom_lengths, num_frags, l)
        plas_seqs = get_seqs(plasfile, plas_start_inds, l)
        chrom_seqs = get_seqs(chromfile, chrom_start_inds, l)
        print('Getting k-mer frequencies')
        (kmer_inds, kmer_count_lens) = utils.compute_kmer_inds(ks)
        pool = mp.Pool(num_procs)
        plas_list = Manager().list()
        for cur in np.arange(len(plas_seqs)):
            plas_list.append(0)
        pool.map(utils.count_kmers, [[ind, s, ks, kmer_inds, kmer_count_lens, plas_list] for (ind, s) in enumerate(plas_seqs)])
        plas_freqs = np.array(plas_list)
        chrom_list = Manager().list()
        for cur in np.arange(len(chrom_seqs)):
            chrom_list.append(0)
        pool.map(utils.count_kmers, [[ind, s, ks, kmer_inds, kmer_count_lens, chrom_list] for (ind, s) in enumerate(chrom_seqs)])
        chrom_freqs = np.array(chrom_list)
        pool.close()
        print('Learning classifier')
        plas_labels = np.ones(plas_freqs.shape[0])
        chrom_labels = np.zeros(chrom_freqs.shape[0])
        data = np.concatenate((plas_freqs, chrom_freqs))
        labels = np.concatenate((plas_labels, chrom_labels))
        scaler = StandardScaler().fit(data)
        scaled = scaler.transform(data)
        clf = LogisticRegression(solver='liblinear').fit(scaled, labels)
        print('Saving classifier')
        clf_name = ('m' + str(l))
        scaler_name = ('s' + str(l))
        dump(clf, os.path.join(outdir, clf_name))
        dump(scaler, os.path.join(outdir, scaler_name))
