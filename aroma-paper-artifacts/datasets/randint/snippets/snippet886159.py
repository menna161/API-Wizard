import datetime
import math
import random
import unittest
from itertools import chain
import genetic


def intercambiar(genesDePadre, donanteGenes, fnObtenerAptitud):
    pares = {Par(donanteGenes[0], donanteGenes[(- 1)]): 0}
    for i in range((len(donanteGenes) - 1)):
        pares[Par(donanteGenes[i], donanteGenes[(i + 1)])] = 0
    genesTemporales = genesDePadre[:]
    if (Par(genesDePadre[0], genesDePadre[(- 1)]) in pares):
        encontró = False
        for i in range((len(genesDePadre) - 1)):
            if (Par(genesDePadre[i], genesDePadre[(i + 1)]) in pares):
                continue
            genesTemporales = (genesDePadre[(i + 1):] + genesDePadre[:(i + 1)])
            encontró = True
            break
        if (not encontró):
            return None
    series = [[genesTemporales[0]]]
    for i in range((len(genesTemporales) - 1)):
        if (Par(genesTemporales[i], genesTemporales[(i + 1)]) in pares):
            series[(- 1)].append(genesTemporales[(i + 1)])
            continue
        series.append([genesTemporales[(i + 1)]])
    aptitudInicial = fnObtenerAptitud(genesDePadre)
    cuenta = random.randint(2, 20)
    índicesDeSerie = range(len(series))
    while (cuenta > 0):
        cuenta -= 1
        for i in índicesDeSerie:
            if (len(series[i]) == 1):
                continue
            if (random.randint(0, len(series)) == 0):
                series[i] = [n for n in reversed(series[i])]
        (índiceA, índiceB) = random.sample(índicesDeSerie, 2)
        (series[índiceA], series[índiceB]) = (series[índiceB], series[índiceA])
        genesDelNiño = list(chain.from_iterable(series))
        if (fnObtenerAptitud(genesDelNiño) > aptitudInicial):
            return genesDelNiño
    return genesDelNiño
