import datetime
import unittest
import genetic


def display(candidate, startTime):
    timeDiff = (datetime.datetime.now() - startTime)
    print('{}\t=> {}\t{}'.format(', '.join(map(str, candidate.Genes)), candidate.Fitness, timeDiff))
