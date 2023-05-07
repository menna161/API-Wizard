import datetime
import random
import unittest
from functools import partial
import genetic


def mostrar(candidato, horaInicio):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    copiaLocal = candidato.Genes[:]
    for i in reversed(range(len(copiaLocal))):
        copiaLocal[i] = str(copiaLocal[i])
    print('\t{}\n{}\n{}'.format('\n\t'.join([d for d in copiaLocal]), candidato.Aptitud, diferencia))
