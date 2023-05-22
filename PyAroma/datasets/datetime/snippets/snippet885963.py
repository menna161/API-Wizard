import datetime
import unittest
import genetic


def mostrar(candidato, horaInicio):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    print('{}\t{}\t{}'.format(''.join(map(str, candidato.Genes)), candidato.Aptitud, diferencia))
