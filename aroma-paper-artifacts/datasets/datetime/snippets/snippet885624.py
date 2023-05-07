import datetime
import math
import random
import sys
import time
import unittest
import genetic


def display(candidate, startTime, bitValues):
    timeDiff = (datetime.datetime.now() - startTime)
    numerator = get_numerator(candidate.Genes, bitValues)
    denominator = get_denominator(candidate.Genes, bitValues)
    print('{}/{}\t{}\t{}'.format(numerator, denominator, candidate.Fitness, timeDiff))
