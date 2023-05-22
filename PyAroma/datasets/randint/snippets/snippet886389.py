import datetime
import random
import unittest
from functools import partial
import genetic


def mutar_mover(genes):
    if (len(genes) < 3):
        return False
    principio = random.choice(range(len(genes)))
    fin = (principio + random.randint(1, 2))
    aMover = genes[principio:fin]
    genes[principio:fin] = []
    índice = random.choice(range(len(genes)))
    if (índice >= principio):
        índice += 1
    genes[índice:índice] = aMover
    return True
