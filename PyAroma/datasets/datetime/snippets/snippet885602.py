import datetime
import math
import random
import unittest
from itertools import chain
import genetic


def display(candidate, startTime):
    timeDiff = (datetime.datetime.now() - startTime)
    print('{}\t{}\t{}\t{}'.format(' '.join(map(str, candidate.Genes)), candidate.Fitness, candidate.Strategy.name, timeDiff))
