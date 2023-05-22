import datetime
import unittest
import genetic


def test(self, tamaño=8):
    geneSet = [i for i in range(tamaño)]
    horaInicio = datetime.datetime.now()

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio, tamaño)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes, tamaño)
    aptitudÓptima = Aptitud(0)
    mejor = genetic.obtener_mejor(fnObtenerAptitud, (2 * tamaño), aptitudÓptima, geneSet, fnMostrar)
    self.assertTrue((not (aptitudÓptima > mejor.Aptitud)))
