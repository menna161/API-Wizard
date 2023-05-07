import datetime
import random
import unittest
from functools import partial
import genetic


def mutate_remove(genes):
    if (len(genes) < 1):
        return False
    del genes[random.randrange(0, len(genes))]
    if ((len(genes) > 1) and (random.randint(0, 1) == 1)):
        del genes[random.randrange(0, len(genes))]
    return True
