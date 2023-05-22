import datetime
import unittest
import genetic


def display(candidate, startTime):
    timeDiff = (datetime.datetime.now() - startTime)
    print('{}...{}\t{:3.2f}\t{}'.format(''.join(map(str, candidate.Genes[:15])), ''.join(map(str, candidate.Genes[(- 15):])), candidate.Fitness, timeDiff))
