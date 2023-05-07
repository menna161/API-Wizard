import datetime
import functools
import operator
import random
import unittest
import genetic


def test(self):
    geneSet = [(i + 1) for i in range(10)]
    horaInicio = datetime.datetime.now()

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes)

    def fnMutar(genes):
        mutar(genes, geneSet)
    aptitudÓptima = Aptitud(36, 360, 0)
    mejor = genetic.obtener_mejor(fnObtenerAptitud, 10, aptitudÓptima, geneSet, fnMostrar, mutación_personalizada=fnMutar)
    self.assertTrue((not (aptitudÓptima > mejor.Aptitud)))
