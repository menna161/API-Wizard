import datetime
import random
import unittest
import genetic


def mostrar(candidato, tamañoDiagonal, horaInicio):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    (filas, columnas, sumaDiagonalNoreste, sumaDiagonalSureste) = obtener_sums(candidato.Genes, tamañoDiagonal)
    for númeroDeFila in range(tamañoDiagonal):
        fila = candidato.Genes[(númeroDeFila * tamañoDiagonal):((númeroDeFila + 1) * tamañoDiagonal)]
        print('\t ', fila, '=', filas[númeroDeFila])
    print(sumaDiagonalNoreste, '\t', columnas, '\t', sumaDiagonalSureste)
    print(' - - - - - - - - - - -', candidato.Aptitud, diferencia)
