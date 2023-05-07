import datetime
from fractions import Fraction
import random
import unittest
import genetic


def mutar(genes, geneSetOrdenado, ventana, geneÍndices):
    índices = (random.sample(geneÍndices, random.randint(1, len(genes))) if (random.randint(0, 10) == 0) else [random.choice(geneÍndices)])
    ventana.deslizar()
    while (len(índices) > 0):
        índice = índices.pop()
        geneSetÍndice = geneSetOrdenado.index(genes[índice])
        principio = max(0, (geneSetÍndice - ventana.Tamaño))
        fin = min((len(geneSetOrdenado) - 1), (geneSetÍndice + ventana.Tamaño))
        geneSetÍndice = random.randint(principio, fin)
        genes[índice] = geneSetOrdenado[geneSetÍndice]
