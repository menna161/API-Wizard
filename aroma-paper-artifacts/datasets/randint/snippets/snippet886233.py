import datetime
import random
import unittest
import genetic
from cortadora import *


def mutar(genes, geneSet, mínGenes, máxGenes, fnObtenerAptitud, rondasMáximas):
    cuenta = random.randint(1, rondasMáximas)
    aptitudInicial = fnObtenerAptitud(genes)
    while (cuenta > 0):
        cuenta -= 1
        if (fnObtenerAptitud(genes) > aptitudInicial):
            return
        añadiendo = ((len(genes) == 0) or ((len(genes) < máxGenes) and (random.randint(0, 5) == 0)))
        if añadiendo:
            genes.append(random.choice(geneSet)())
            continue
        eliminando = ((len(genes) > mínGenes) and (random.randint(0, 50) == 0))
        if eliminando:
            índice = random.randrange(0, len(genes))
            del genes[índice]
            continue
        índice = random.randrange(0, len(genes))
        genes[índice] = random.choice(geneSet)()
