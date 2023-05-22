import datetime
import functools
import operator
import random
import unittest
import genetic


def mostrar(candidato, horaInicio):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    print('{} - {}\t{}\t{}'.format(', '.join(map(str, candidato.Genes[0:5])), ', '.join(map(str, candidato.Genes[5:10])), candidato.Aptitud, diferencia))
