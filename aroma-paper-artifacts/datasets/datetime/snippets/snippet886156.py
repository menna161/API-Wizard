import datetime
import math
import random
import unittest
from itertools import chain
import genetic


def mostrar(candidato, horaInicio):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    print('{}\t{}\t{}\t{}'.format(' '.join(map(str, candidato.Genes)), candidato.Aptitud, candidato.Estrategia.name, diferencia))
