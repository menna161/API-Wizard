import datetime
import random
import unittest
from functools import partial
import genetic


def display(candidate, startTime):
    timeDiff = (datetime.datetime.now() - startTime)
    localCopy = candidate.Genes[:]
    for i in reversed(range(len(localCopy))):
        localCopy[i] = str(localCopy[i])
    print('\t{}\n{}\n{}'.format('\n\t'.join([d for d in localCopy]), candidate.Fitness, timeDiff))
