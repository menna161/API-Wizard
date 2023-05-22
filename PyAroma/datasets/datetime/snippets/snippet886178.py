import datetime
import math
import random
import sys
import time
import unittest
import genetic


def mostrar(candidato, horaInicio, valoresDeBits):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    numerador = obtener_numerador(candidato.Genes, valoresDeBits)
    denominator = obtener_denominador(candidato.Genes, valoresDeBits)
    print('{}/{}\t{}\t{}'.format(numerador, denominator, candidato.Aptitud, diferencia))
