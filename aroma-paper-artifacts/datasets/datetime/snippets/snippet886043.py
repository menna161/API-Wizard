import datetime
import random
import unittest
import genetic


def generar(self, tamañoDiagonal, edadMáxima):
    nCuadrado = (tamañoDiagonal * tamañoDiagonal)
    geneSet = [i for i in range(1, (nCuadrado + 1))]
    sumaEsperada = ((tamañoDiagonal * (nCuadrado + 1)) / 2)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes, tamañoDiagonal, sumaEsperada)

    def fnMostrar(candidato):
        mostrar(candidato, tamañoDiagonal, horaInicio)
    geneÍndices = [i for i in range(0, len(geneSet))]

    def fnMutar(genes):
        mutar(genes, geneÍndices)

    def fnCreaciónPersonalizada():
        return random.sample(geneSet, len(geneSet))
    valorÓptimo = Aptitud(0)
    horaInicio = datetime.datetime.now()
    mejor = genetic.obtener_mejor(fnObtenerAptitud, nCuadrado, valorÓptimo, geneSet, fnMostrar, fnMutar, fnCreaciónPersonalizada, edadMáxima)
    self.assertTrue((not (valorÓptimo > mejor.Aptitud)))
