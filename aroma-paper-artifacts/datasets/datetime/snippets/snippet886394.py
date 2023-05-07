import datetime
import random
import unittest
from functools import partial
import genetic


def test_conocimiento_perfecto(self):
    mínGenes = 10
    máxGenes = 20
    geneSet = crear_geneSet()
    horaInicio = datetime.datetime.now()

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes)
    recuentoDeMutaciones = [1]
    operadoresDeMutación = [partial(mutar_añadir, geneSet=geneSet), partial(mutar_reemplazar, geneSet=geneSet), mutar_remover, mutar_intercambiar_adyacente, mutar_mover]

    def fnMutar(genes):
        mutar(genes, fnObtenerAptitud, operadoresDeMutación, recuentoDeMutaciones)

    def fnIntercambio(padre, donante):
        niño = (padre[0:int((len(padre) / 2))] + donante[int((len(donante) / 2)):])
        fnMutar(niño)
        return niño

    def fnCrear():
        return random.sample(geneSet, random.randrange(mínGenes, máxGenes))
    aptitudÓptima = Aptitud(620, 120, 0, 11)
    mejor = genetic.obtener_mejor(fnObtenerAptitud, mínGenes, aptitudÓptima, None, fnMostrar, fnMutar, fnCrear, edadMáxima=500, tamañoDePiscina=20, intercambiar=fnIntercambio)
    self.assertTrue((not (aptitudÓptima > mejor.Aptitud)))
