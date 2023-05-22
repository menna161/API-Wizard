import datetime
import unittest
import genetic


def ordenar_números(self, númerosTotales):
    geneSet = [i for i in range(100)]
    horaInicio = datetime.datetime.now()

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes)
    aptitudÓptima = Aptitud(númerosTotales, 0)
    mejor = genetic.obtener_mejor(fnObtenerAptitud, númerosTotales, aptitudÓptima, geneSet, fnMostrar)
    self.assertTrue((not (aptitudÓptima > mejor.Aptitud)))
