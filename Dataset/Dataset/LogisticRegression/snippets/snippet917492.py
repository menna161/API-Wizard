import numpy as np
import os
from sklearn.linear_model import LogisticRegression
from sklearn.preprocessing import StandardScaler
from joblib import load
import multiprocessing as mp
from multiprocessing import Manager
import plasclass.plasclass_utils as utils


def classify(self, seq):
    'Classify the sequence(s), return the probability of the sequence(s) being a plasmid.\n        Assumes seq is either an individual string or a list of strings\n        Returns either an individual plasmid probability for seq or a list of\n        plasmid probabilities for each sequence in seq\n        '
    if isinstance(seq, str):
        print('Counting k-mers for sequence of length {}'.format(len(seq)))
        kmer_freqs = [0]
        scale = self._get_scale(len(seq))
        utils.count_kmers([0, seq, self._ks, self._kmer_inds, self._kmer_count_lens, kmer_freqs])
        kmer_freqs = np.array(kmer_freqs)
        standardized_freqs = self._standardize(kmer_freqs, scale)
        print('Classifying')
        return self.classifiers[scale]['clf'].predict_proba(standardized_freqs)[(0, 1)]
    elif isinstance(seq, list):
        print('{} sequences to classify. Classifying in batches of 100k'.format(len(seq)))
        results = []
        seq_ind = 0
        pool = mp.Pool(self._n_procs)
        while (seq_ind < len(seq)):
            print('Starting new batch')
            seq_batch = seq[seq_ind:(seq_ind + 100000)]
            scales = [self._get_scale(len(s)) for s in seq_batch]
            scale_partitions = {s: [seq_batch[i] for (i, v) in enumerate(scales) if (v == s)] for s in self._scales}
            partitioned_classifications = {}
            for scale in self._scales:
                part_seqs = scale_partitions[scale]
                if (len(part_seqs) <= 0):
                    continue
                print('Getting kmer frequencies for partition length {}'.format(scale))
                shared_list = Manager().list()
                for cur in np.arange(len(part_seqs)):
                    shared_list.append(0)
                pool.map(utils.count_kmers, [[ind, s, self._ks, self._kmer_inds, self._kmer_count_lens, shared_list] for (ind, s) in enumerate(part_seqs)])
                kmer_freqs_mat = np.array(shared_list)
                standardized_freqs = self._standardize(kmer_freqs_mat, scale)
                print('Classifying sequences of length scale {}'.format(scale))
                partitioned_classifications[scale] = self.classifiers[scale]['clf'].predict_proba(standardized_freqs)[(:, 1)]
            scale_inds = {s: 0 for s in self._scales}
            for s in scales:
                results.append(partitioned_classifications[s][scale_inds[s]])
                scale_inds[s] += 1
            seq_ind += 100000
        pool.close()
        return np.array(results)
    else:
        raise TypeError('Can only classify strings or lists of strings')
