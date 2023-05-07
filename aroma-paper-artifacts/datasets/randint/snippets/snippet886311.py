import datetime
import random
import unittest
import circuitos
import genetic


def crear_gen(índice, puertas, fuentes):
    if (índice < len(fuentes)):
        tipoDePuerta = fuentes[índice]
    else:
        tipoDePuerta = random.choice(puertas)
    índiceA = índiceB = None
    if (tipoDePuerta[1].recuento_de_entradas() > 0):
        índiceA = random.randint(0, índice)
    if (tipoDePuerta[1].recuento_de_entradas() > 1):
        índiceB = random.randint(0, índice)
        if (índiceB == índiceA):
            índiceB = random.randint(0, índice)
    return Nodo(tipoDePuerta[0], índiceA, índiceB)
