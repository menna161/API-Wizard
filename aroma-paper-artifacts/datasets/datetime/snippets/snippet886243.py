import datetime
import random
import unittest
import genetic
from cortadora import *


def ejecutar_con(self, geneSet, anchura, altura, mínGenes, máxGenes, númeroEsperadoDeInstrucciones, rondasMáximasDeMutación, fnCrearCampo, númeroEsperadoDePasos):
    ubicaciónInicialDelCortador = Ubicación(int((anchura / 2)), int((altura / 2)))
    direcciónInicialDelCortador = Direcciones.Sur.value

    def fnCrear():
        return crear(geneSet, 1, altura)

    def fnEvaluar(instrucciones):
        programa = Programa(instrucciones)
        cortadora = Cortadora(ubicaciónInicialDelCortador, direcciónInicialDelCortador)
        campo = fnCrearCampo()
        try:
            programa.evaluar(cortadora, campo)
        except RecursionError:
            pass
        return (campo, cortadora, programa)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes, fnEvaluar)
    horaInicio = datetime.datetime.now()

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio, fnEvaluar)

    def fnMutar(niño):
        mutar(niño, geneSet, mínGenes, máxGenes, fnObtenerAptitud, rondasMáximasDeMutación)
    aptitudÓptima = Aptitud((anchura * altura), númeroEsperadoDeInstrucciones, númeroEsperadoDePasos)
    mejor = genetic.obtener_mejor(fnObtenerAptitud, None, aptitudÓptima, None, fnMostrar, fnMutar, fnCrear, edadMáxima=None, tamañoDePiscina=10, intercambiar=intercambiar)
    self.assertTrue((not (aptitudÓptima > mejor.Aptitud)))
