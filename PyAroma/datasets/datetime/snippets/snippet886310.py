import datetime
import random
import unittest
import circuitos
import genetic


def mostrar(candidato, horaInicio):
    circuito = nodos_a_circuito(candidato.Genes)[0]
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    print('{}\t{}\t{}'.format(circuito, candidato.Aptitud, diferencia))
