from __future__ import print_function
import sys
import os
import numpy as np
import hashlib
import random
import preprocess


def run_with_train_valid_test_corpus(self, train_file, valid_file, test_file):
    "\n        Run with pre-splited train_file, valid_file, test_file\n        The input format should be label \t text1 \t text2\n        The query ids can't be duplicated. For the same query\n        id, the document ids can't be duplicated.\n        Note that if we make queries with unique id (fixed 10 candidates for a single query), then it is\n        possible that multiple queries have different query ids, but with the same text (in rare cases)\n        :param train_file: train file\n        :param valid_file: valid file\n        :param test_file: test file\n        :return: corpus, rels_train, rels_valid, rels_test\n        "
    hashid = {}
    corpus = {}
    rels = []
    rels_train = []
    rels_valid = []
    rels_test = []
    curQ = 'init'
    curQid = 0
    for file_path in list([train_file, valid_file, test_file]):
        if (file_path == train_file):
            rels = rels_train
        elif (file_path == valid_file):
            rels = rels_valid
        if (file_path == test_file):
            rels = rels_test
        f = open(file_path, 'r')
        for line in f:
            line = line.decode('utf8')
            line = line.strip()
            (label, t1, t2) = self.parse_line(line)
            id2 = self.get_text_id(hashid, t2, 'D')
            if (t1 == curQ):
                id1 = ('Q' + str(curQid))
            else:
                curQid += 1
                id1 = ('Q' + str(curQid))
                curQ = t1
            corpus[id1] = t1
            corpus[id2] = t2
            rels.append((label, id1, id2))
        f.close()
    return (corpus, rels_train, rels_valid, rels_test)
