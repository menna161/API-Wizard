import datetime
import random
import unittest
import genetic
import lawnmower


def display(candidate, startTime, fnEvaluate):
    (field, mower, program) = fnEvaluate(candidate.Genes)
    timeDiff = (datetime.datetime.now() - startTime)
    field.display(mower)
    print('{}\t{}'.format(candidate.Fitness, timeDiff))
    program.print()
