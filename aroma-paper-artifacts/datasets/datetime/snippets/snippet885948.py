import datetime
import unittest
import genetic


def mostrar(candidato, horaInicio, tamaño):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    tablero = Tablero(candidato.Genes, tamaño)
    tablero.print()
    print('{}\t- {}\t{}'.format(' '.join(map(str, candidato.Genes)), candidato.Aptitud, diferencia))
