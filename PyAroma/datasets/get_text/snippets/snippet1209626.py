from __future__ import print_function
import sys
import os
import numpy as np
import hashlib
import random
import preprocess


def run_with_two_corpus(self, file_path):
    hashid_q = {}
    hashid_d = {}
    corpus_q = {}
    corpus_d = {}
    rels = []
    f = open(file_path, 'r')
    for line in f:
        line = line.decode('utf8')
        line = line.strip()
        (label, t1, t2) = self.parse_line(line)
        id1 = self.get_text_id(hashid_q, t1, 'Q')
        id2 = self.get_text_id(hashid_d, t2, 'D')
        corpus_q[id1] = t1
        corpus_d[id2] = t2
        rels.append((label, id1, id2))
    f.close()
    return (corpus_q, corpus_d, rels)
