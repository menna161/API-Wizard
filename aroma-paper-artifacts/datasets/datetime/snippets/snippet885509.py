import datetime
import random
import sys
import unittest
import genetic


def display(candidate, startTime):
    timeDiff = (datetime.datetime.now() - startTime)
    genes = candidate.Genes[:]
    genes.sort(key=(lambda iq: iq.Quantity), reverse=True)
    descriptions = [((str(iq.Quantity) + 'x') + iq.Item.Name) for iq in genes]
    if (len(descriptions) == 0):
        descriptions.append('Empty')
    print('{}\t{}\t{}'.format(', '.join(descriptions), candidate.Fitness, timeDiff))
