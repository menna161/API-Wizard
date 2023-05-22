import datetime
import random
import unittest
import genetic


def mostrar(candidato, horaInicio, tableroAncho, tableroAltura):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    tablero = Tablero(candidato.Genes, tableroAncho, tableroAltura)
    tablero.print()
    print('{}\n\t{}\t{}'.format(' '.join(map(str, candidato.Genes)), candidato.Aptitud, diferencia))
