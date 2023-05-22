import datetime
import random
import unittest
import genetic


def adivine_contraseña(self, objetivo):
    horaInicio = datetime.datetime.now()

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes, objetivo)

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio)
    aptitudÓptima = len(objetivo)
    mejor = genetic.obtener_mejor(fnObtenerAptitud, len(objetivo), aptitudÓptima, self.geneSet, fnMostrar)
    self.assertEqual(mejor.Genes, objetivo)
