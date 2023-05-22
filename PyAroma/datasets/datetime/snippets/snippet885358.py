import datetime
import random
import unittest
import genetic


def display(candidate, startTime):
    timeDiff = (datetime.datetime.now() - startTime)
    print('{}\t{}\t{}'.format(''.join(candidate.Genes), candidate.Fitness, timeDiff))
