import datetime
from fractions import Fraction
import random
import unittest
import genetic


def mostrar(candidato, horaInicio, fnGenesAEntradas):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    símbolos = 'xyza'
    resultado = ', '.join(('{} = {}'.format(s, v) for (s, v) in zip(símbolos, fnGenesAEntradas(candidato.Genes))))
    print('{}\t{}\t{}'.format(resultado, candidato.Aptitud, diferencia))
