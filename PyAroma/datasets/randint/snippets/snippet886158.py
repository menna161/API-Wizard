import datetime
import math
import random
import unittest
from itertools import chain
import genetic


def mutar(genes, fnObtenerAptitud):
    cuenta = random.randint(2, len(genes))
    aptitudInicial = fnObtenerAptitud(genes)
    while (cuenta > 0):
        cuenta -= 1
        (índiceA, índiceB) = random.sample(range(len(genes)), 2)
        (genes[índiceA], genes[índiceB]) = (genes[índiceB], genes[índiceA])
        aptitud = fnObtenerAptitud(genes)
        if (aptitud > aptitudInicial):
            return
