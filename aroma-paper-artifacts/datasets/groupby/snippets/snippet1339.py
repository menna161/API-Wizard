from __future__ import print_function
import itertools
import operator
import optparse
import sys


def doOneFile(opts, lines):
    alignments = mafInput(opts, lines)
    for (k, v) in itertools.groupby(alignments, operator.itemgetter(0)):
        doOneQuery(opts, k, list(v))
