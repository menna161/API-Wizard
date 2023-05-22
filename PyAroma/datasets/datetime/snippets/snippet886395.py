import datetime
import random
import unittest
from functools import partial
import genetic


def test_tornament(self):
    mínGenes = 10
    máxGenes = 20
    geneSet = crear_geneSet()
    horaInicio = datetime.datetime.now()

    def fnMostrar(genes, ganados, empates, perdidos, generación):
        print('-- generación {} --'.format(generación))
        mostrar(genetic.Cromosoma(genes, Aptitud(ganados, empates, perdidos, len(genes)), None), horaInicio)
    recuentoDeMutaciones = [1]
    operadoresDeMutación = [partial(mutar_añadir, geneSet=geneSet), partial(mutar_reemplazar, geneSet=geneSet), mutar_remover, mutar_intercambiar_adyacente, mutar_mover]

    def fnMutar(genes):
        mutar(genes, (lambda x: 0), operadoresDeMutación, recuentoDeMutaciones)

    def fnIntercambio(padre, donante):
        niño = (padre[0:int((len(padre) / 2))] + donante[int((len(donante) / 2)):])
        fnMutar(niño)
        return niño

    def fnCrear():
        return random.sample(geneSet, random.randrange(mínGenes, máxGenes))

    def fnClaveDeOrden(genes, ganados, empates, perdidos):
        return ((((- 1000) * perdidos) - empates) + (1 / len(genes)))
    genetic.torneo(fnCrear, fnIntercambio, jugar1en1, fnMostrar, fnClaveDeOrden, 13)
