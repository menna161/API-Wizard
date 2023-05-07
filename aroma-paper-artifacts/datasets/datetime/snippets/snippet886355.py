import datetime
import random
import re
import unittest
from functools import partial
import genetic


def encontrar_regex(self, deseadas, noDeseadas, longitudEsperada, operadoresPersonalizados=None):
    horaInicio = datetime.datetime.now()
    genesDeTexto = (deseadas | set((c for w in deseadas for c in w)))
    geneSet = [i for i in (todosMetacaracteres | genesDeTexto)]

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes, deseadas, noDeseadas)
    recuentoDeMutaciones = [1]
    operadoresDeMutación = [partial(mutar_añadir, geneSet=geneSet), partial(mutar_reemplazar, geneSet=geneSet), mutar_remover, mutar_intercambiar, mutar_mover]
    if (operadoresPersonalizados is not None):
        operadoresDeMutación.extend(operadoresPersonalizados)

    def fnMutar(genes):
        mutar(genes, fnObtenerAptitud, operadoresDeMutación, recuentoDeMutaciones)
    aptitudÓptima = Aptitud(len(deseadas), len(deseadas), 0, longitudEsperada)
    mejor = genetic.obtener_mejor(fnObtenerAptitud, max((len(i) for i in genesDeTexto)), aptitudÓptima, geneSet, fnMostrar, fnMutar, tamañoDePiscina=10)
    self.assertTrue((not (aptitudÓptima > mejor.Aptitud)))
    for info in erroresEnRegexes.values():
        print('')
        print(info[0])
        print(info[1])
        print(info[2])
