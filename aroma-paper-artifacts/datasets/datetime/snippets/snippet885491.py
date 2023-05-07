import datetime
import random
import unittest
import genetic


def display(candidate, diagonalSize, startTime):
    timeDiff = (datetime.datetime.now() - startTime)
    (rows, columns, northeastDiagonalSum, southeastDiagonalSum) = get_sums(candidate.Genes, diagonalSize)
    for rowNumber in range(diagonalSize):
        row = candidate.Genes[(rowNumber * diagonalSize):((rowNumber + 1) * diagonalSize)]
        print('\t ', row, '=', rows[rowNumber])
    print(northeastDiagonalSum, '\t', columns, '\t', southeastDiagonalSum)
    print(' - - - - - - - - - - -', candidate.Fitness, timeDiff)
