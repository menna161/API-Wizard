import datetime
import unittest
import genetic


def display(candidate, startTime, size):
    timeDiff = (datetime.datetime.now() - startTime)
    board = Board(candidate.Genes, size)
    board.print()
    print('{}\t- {}\t{}'.format(' '.join(map(str, candidate.Genes)), candidate.Fitness, timeDiff))
