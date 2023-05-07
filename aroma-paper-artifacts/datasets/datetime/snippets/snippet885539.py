import datetime
from fractions import Fraction
import random
import unittest
import genetic


def display(candidate, startTime, fnGenesToInputs):
    timeDiff = (datetime.datetime.now() - startTime)
    symbols = 'xyza'
    result = ', '.join(('{} = {}'.format(s, v) for (s, v) in zip(symbols, fnGenesToInputs(candidate.Genes))))
    print('{}\t{}\t{}'.format(result, candidate.Fitness, timeDiff))
