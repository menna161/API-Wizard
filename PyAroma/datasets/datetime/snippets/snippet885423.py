import datetime
import functools
import operator
import random
import unittest
import genetic


def display(candidate, startTime):
    timeDiff = (datetime.datetime.now() - startTime)
    print('{} - {}\t{}\t{}'.format(', '.join(map(str, candidate.Genes[0:5])), ', '.join(map(str, candidate.Genes[5:10])), candidate.Fitness, timeDiff))
