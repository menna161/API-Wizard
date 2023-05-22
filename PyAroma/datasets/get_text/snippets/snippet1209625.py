from __future__ import print_function
import sys
import os
import numpy as np
import hashlib
import random
import preprocess


def run_with_one_corpus(self, file_path):
    hashid = {}
    corpus = {}
    rels = []
    f = open(file_path, 'r')
    for line in f:
        line = line.decode('utf8')
        line = line.strip()
        (label, t1, t2) = self.parse_line(line)
        id1 = self.get_text_id(hashid, t1, 'T')
        id2 = self.get_text_id(hashid, t2, 'T')
        corpus[id1] = t1
        corpus[id2] = t2
        rels.append((label, id1, id2))
    f.close()
    return (corpus, rels)
