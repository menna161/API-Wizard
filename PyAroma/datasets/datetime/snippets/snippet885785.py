import datetime
import random
import re
import unittest
from functools import partial
import genetic


def display(candidate, startTime):
    timeDiff = (datetime.datetime.now() - startTime)
    print('{}\t{}\t{}'.format(repair_regex(candidate.Genes), candidate.Fitness, timeDiff))
