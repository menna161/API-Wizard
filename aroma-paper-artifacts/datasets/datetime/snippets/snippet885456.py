import datetime
import random
import unittest
import genetic


def display(candidate, startTime, boardWidth, boardHeight):
    timeDiff = (datetime.datetime.now() - startTime)
    board = Board(candidate.Genes, boardWidth, boardHeight)
    board.print()
    print('{}\n\t{}\t{}'.format(' '.join(map(str, candidate.Genes)), candidate.Fitness, timeDiff))
