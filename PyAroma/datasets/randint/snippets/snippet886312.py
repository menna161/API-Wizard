import datetime
import random
import unittest
import circuitos
import genetic


def mutar(genesDelNiño, fnCrearGen, fnObtenerAptitud, fuenteCount):
    cuenta = random.randint(1, 5)
    aptitudInicial = fnObtenerAptitud(genesDelNiño)
    while (cuenta > 0):
        cuenta -= 1
        índicesUsados = [i for i in nodos_a_circuito(genesDelNiño)[1] if (i >= fuenteCount)]
        if (len(índicesUsados) == 0):
            return
        índice = random.choice(índicesUsados)
        genesDelNiño[índice] = fnCrearGen(índice)
        if (fnObtenerAptitud(genesDelNiño) > aptitudInicial):
            return
