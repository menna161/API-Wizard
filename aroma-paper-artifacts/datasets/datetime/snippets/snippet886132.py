import datetime
import random
import unittest
import genetic


def test(self):
    geneSet = [i for i in range(1, (9 + 1))]
    horaInicio = datetime.datetime.now()
    valorÓptimo = 100

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio)
    reglasDeValidación = construir_las_reglas_de_validación()

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes, reglasDeValidación)

    def fnCrear():
        return random.sample((geneSet * 9), 81)

    def fnMutar(genes):
        mutar(genes, reglasDeValidación)
    mejor = genetic.obtener_mejor(fnObtenerAptitud, None, valorÓptimo, None, fnMostrar, fnMutar, fnCrear, edadMáxima=50)
    self.assertEqual(mejor.Aptitud, valorÓptimo)
