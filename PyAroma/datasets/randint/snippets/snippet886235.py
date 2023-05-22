import datetime
import random
import unittest
import genetic
from cortadora import *


def intercambiar(padre, otroPadre):
    genesDelNiño = padre[:]
    if ((len(padre) <= 2) or (len(otroPadre) < 2)):
        return genesDelNiño
    longitud = random.randint(1, (len(padre) - 2))
    principio = random.randrange(0, (len(padre) - longitud))
    genesDelNiño[principio:(principio + longitud)] = otroPadre[principio:(principio + longitud)]
    return genesDelNiño
