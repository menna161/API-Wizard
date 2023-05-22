import datetime
import random
import re
import unittest
from functools import partial
import genetic


def mutate_move(genes):
    if (len(genes) < 3):
        return False
    start = random.choice(range(len(genes)))
    stop = (start + random.randint(1, 2))
    toMove = genes[start:stop]
    genes[start:stop] = []
    index = random.choice(range(len(genes)))
    if (index >= start):
        index += 1
    genes[index:index] = toMove
    return True
