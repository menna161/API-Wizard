import datetime
import random
import unittest
import genetic


def mostrar(candidato, horaInicio):
    diferencia = (datetime.datetime.now() - horaInicio).total_seconds()
    for filaId in range(9):
        fila = ' | '.join((' '.join((str(i) for i in candidato.Genes[((filaId * 9) + i):(((filaId * 9) + i) + 3)])) for i in [0, 3, 6]))
        print('', fila)
        if ((filaId < 8) and ((filaId % 3) == 2)):
            print(' ----- + ----- + -----')
    print(' - = -   - = -   - = - {}\t{}\n'.format(candidato.Aptitud, diferencia))
