import datetime
from fractions import Fraction
import random
import unittest
import genetic


def resolver_desconocidos(self, numUnknowns, geneSet, ecuaciones, fnGenesAEntradas):
    horaInicio = datetime.datetime.now()
    edadMáxima = 50
    ventana = Ventana(max(1, int((len(geneSet) / (2 * edadMáxima)))), max(1, int((len(geneSet) / 3))), int((len(geneSet) / 2)))
    geneÍndices = [i for i in range(numUnknowns)]
    geneSetOrdenado = sorted(geneSet)

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio, fnGenesAEntradas)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes, ecuaciones)

    def fnMutar(genes):
        mutar(genes, geneSetOrdenado, ventana, geneÍndices)
    aptitudÓptima = Aptitud(0)
    mejor = genetic.obtener_mejor(fnObtenerAptitud, numUnknowns, aptitudÓptima, geneSet, fnMostrar, fnMutar, edadMáxima=edadMáxima)
    self.assertTrue((not (aptitudÓptima > mejor.Aptitud)))
