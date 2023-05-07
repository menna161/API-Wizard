import datetime
import random
import unittest
import genetic


def mutar(genes, números, operaciones, númerosMin, númerosMax, fnObtenerAptitud):
    cuenta = random.randint(1, 10)
    aptitudInicial = fnObtenerAptitud(genes)
    while (cuenta > 0):
        cuenta -= 1
        if (fnObtenerAptitud(genes) > aptitudInicial):
            return
        cuentaDeNúmeros = ((1 + len(genes)) / 2)
        añadiendo = ((cuentaDeNúmeros < númerosMax) and (random.randint(0, 100) == 0))
        if añadiendo:
            genes.append(random.choice(operaciones))
            genes.append(random.choice(números))
            continue
        eliminando = ((cuentaDeNúmeros > númerosMin) and (random.randint(0, 20) == 0))
        if eliminando:
            índice = random.randrange(0, (len(genes) - 1))
            del genes[índice]
            del genes[índice]
            continue
        índice = random.randrange(0, len(genes))
        genes[índice] = (random.choice(operaciones) if ((índice & 1) == 1) else random.choice(números))
