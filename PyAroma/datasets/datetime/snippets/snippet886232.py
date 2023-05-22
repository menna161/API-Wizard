import datetime
import random
import unittest
import genetic
from cortadora import *


def mostrar(candidato, horaInicio, fnEvaluar):
    (campo, cortadora, programa) = fnEvaluar(candidato.Genes)
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    campo.mostrar(cortadora)
    print('{}\t{}'.format(candidato.Aptitud, diferencia))
    programa.print()
