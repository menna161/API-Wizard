import datetime
import random
import unittest
import genetic


def create(numbers, operations, minNumbers, maxNumbers):
    genes = [random.choice(numbers)]
    count = random.randint(minNumbers, (1 + maxNumbers))
    while (count > 1):
        count -= 1
        genes.append(random.choice(operations))
        genes.append(random.choice(numbers))
    return genes
