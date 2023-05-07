import datetime
import unittest
import genetic


def mostrar(candidato, horaInicio):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    print('{}...{}\t{:3.2f}\t{}'.format(''.join(map(str, candidato.Genes[:15])), ''.join(map(str, candidato.Genes[(- 15):])), candidato.Aptitud, diferencia))
