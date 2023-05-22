import datetime
import unittest
import genetic


def test(self, longitud=100):
    geneSet = [0, 1]
    horaInicio = datetime.datetime.now()

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes)
    aptitudÓptima = longitud
    mejor = genetic.obtener_mejor(fnObtenerAptitud, longitud, aptitudÓptima, geneSet, fnMostrar)
    self.assertEqual(mejor.Aptitud, aptitudÓptima)
