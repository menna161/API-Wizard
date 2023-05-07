import datetime
import random
import unittest
import genetic


def crear(números, operaciones, númerosMin, númerosMax):
    genes = [random.choice(números)]
    cuenta = random.randint(númerosMin, (1 + númerosMax))
    while (cuenta > 1):
        cuenta -= 1
        genes.append(random.choice(operaciones))
        genes.append(random.choice(números))
    return genes
