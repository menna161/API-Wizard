import datetime
import random
import unittest
import genetic
from cortadora import *


def crear(geneSet, mínGenes, máxGenes):
    cantidad = random.randint(mínGenes, máxGenes)
    genes = [random.choice(geneSet)() for _ in range(1, cantidad)]
    return genes
