import datetime
import random
import unittest
import genetic


def mostrar(candidato, horaInicio):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    print('{}\t{}\t{}'.format(' '.join(map(str, [i for i in candidato.Genes])), candidato.Aptitud, diferencia))
