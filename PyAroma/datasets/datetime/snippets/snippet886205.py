import datetime
import random
import unittest
import genetic


def resolver(self, operaciones, operacionesPriorizadas, soluciónDeLongitudÓptima):
    números = [1, 2, 3, 4, 5, 6, 7]
    totalEsperado = evaluar(soluciónDeLongitudÓptima, operacionesPriorizadas)
    númerosMin = ((1 + len(soluciónDeLongitudÓptima)) / 2)
    númerosMax = (6 * númerosMin)
    horaInicio = datetime.datetime.now()

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio)

    def fnEvaluar(genes):
        return evaluar(genes, operacionesPriorizadas)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes, totalEsperado, fnEvaluar)

    def fnCrear():
        return crear(números, operaciones, númerosMin, númerosMax)

    def fnMutar(niño):
        mutar(niño, números, operaciones, númerosMin, númerosMax, fnObtenerAptitud)
    aptitudÓptima = fnObtenerAptitud(soluciónDeLongitudÓptima)
    mejor = genetic.obtener_mejor(fnObtenerAptitud, None, aptitudÓptima, None, fnMostrar, fnMutar, fnCrear, edadMáxima=50)
    self.assertTrue((not (aptitudÓptima > mejor.Aptitud)))
