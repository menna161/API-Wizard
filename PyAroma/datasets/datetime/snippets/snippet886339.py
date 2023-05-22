import datetime
import random
import re
import unittest
from functools import partial
import genetic


def mostrar(candidato, horaInicio):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    print('{}\t{}\t{}'.format(reparar_regex(candidato.Genes), candidato.Aptitud, diferencia))
