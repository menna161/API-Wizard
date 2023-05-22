import datetime
import random
import unittest
import circuitos
import genetic


def encontrar_circuito(self, reglas, longitudEsperada):
    horaInicio = datetime.datetime.now()

    def fnMostrar(candidato, longitud=None):
        if (longitud is not None):
            print('-- nodos distintos en el circuito:', len(nodos_a_circuito(candidato.Genes)[1]))
        mostrar(candidato, horaInicio)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes, reglas, self.entradas)

    def fnCrearGen(índice):
        return crear_gen(índice, self.puertas, self.fuentes)

    def fnMutar(genes):
        mutar(genes, fnCrearGen, fnObtenerAptitud, len(self.fuentes))
    longitudMáxima = 50

    def fnCrear():
        return [fnCrearGen(i) for i in range(longitudMáxima)]

    def fnFunciónDeOptimización(longitudVariable):
        nonlocal longitudMáxima
        longitudMáxima = longitudVariable
        return genetic.obtener_mejor(fnObtenerAptitud, None, len(reglas), None, fnMostrar, fnMutar, fnCrear, tamañoDePiscina=3, segundosMáximos=30)

    def fnEsUnaMejora(mejorActual, niño):
        return ((niño.Aptitud == len(reglas)) and (len(nodos_a_circuito(niño.Genes)[1]) < len(nodos_a_circuito(mejorActual.Genes)[1])))

    def fnEsÓptimo(niño):
        return ((niño.Aptitud == len(reglas)) and (len(nodos_a_circuito(niño.Genes)[1]) <= longitudEsperada))

    def fnObtenerValorDeCaracterísticaSiguiente(mejorActual):
        return len(nodos_a_circuito(mejorActual.Genes)[1])
    mejor = genetic.ascenso_de_la_colina(fnFunciónDeOptimización, fnEsUnaMejora, fnEsÓptimo, fnObtenerValorDeCaracterísticaSiguiente, fnMostrar, longitudMáxima)
    self.assertTrue((mejor.Aptitud == len(reglas)))
    self.assertFalse((len(nodos_a_circuito(mejor.Genes)[1]) > longitudEsperada))
