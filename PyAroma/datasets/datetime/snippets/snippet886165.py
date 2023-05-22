import datetime
import math
import random
import unittest
from itertools import chain
import genetic


def resolver(self, búsquedaDeUbicación, secuenciaÓptima):
    geneSet = [i for i in búsquedaDeUbicación.keys()]

    def fnCrear():
        return random.sample(geneSet, len(geneSet))

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes, búsquedaDeUbicación)

    def fnMutar(genes):
        mutar(genes, fnObtenerAptitud)

    def fnIntercambio(padre, donante):
        return intercambiar(padre, donante, fnObtenerAptitud)
    aptitudÓptima = fnObtenerAptitud(secuenciaÓptima)
    horaInicio = datetime.datetime.now()
    mejor = genetic.obtener_mejor(fnObtenerAptitud, None, aptitudÓptima, None, fnMostrar, fnMutar, fnCrear, edadMáxima=500, tamañoDePiscina=25, intercambiar=fnIntercambio)
    self.assertTrue((not (aptitudÓptima > mejor.Aptitud)))
