import datetime
import random
import sys
import unittest
import genetic


def mostrar(candidato, horaInicio):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    genes = candidato.Genes[:]
    genes.sort(key=(lambda ac: ac.Cantidad), reverse=True)
    descripciones = [((str(ac.Cantidad) + 'x') + ac.Artículo.Nombre) for ac in genes]
    if (len(descripciones) == 0):
        descripciones.append('Vacío')
    print('{}\t{}\t{}'.format(', '.join(descripciones), candidato.Aptitud, diferencia))
