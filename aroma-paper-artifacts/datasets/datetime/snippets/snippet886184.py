import datetime
import math
import random
import sys
import time
import unittest
import genetic


def test(self, valoresDeBits=[512, 256, 128, 64, 32, 16, 8, 4, 2, 1], segundosMáximos=None):
    geneSet = [i for i in range(2)]
    horaInicio = datetime.datetime.now()

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio, valoresDeBits)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes, valoresDeBits)
    aptitudÓptima = 3.14159

    def fnMutar(genes):
        mutar(genes, len(valoresDeBits))
    longitud = (2 * len(valoresDeBits))
    mejor = genetic.obtener_mejor(fnObtenerAptitud, longitud, aptitudÓptima, geneSet, fnMostrar, fnMutar, edadMáxima=250, segundosMáximos=segundosMáximos)
    return (aptitudÓptima <= mejor.Aptitud)
