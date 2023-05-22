import datetime
import random
import unittest
import genetic


def mutar(genes, reglasDeValidación):
    reglaSeleccionada = next((regla for regla in reglasDeValidación if (genes[regla.Índice] == genes[regla.OtroÍndice])))
    if (reglaSeleccionada is None):
        return
    if (((índice_fila(reglaSeleccionada.OtroÍndice) % 3) == 2) and (random.randint(0, 10) == 0)):
        secciónPrincipio = sección_principio(reglaSeleccionada.Índice)
        actual = reglaSeleccionada.OtroÍndice
        while (reglaSeleccionada.OtroÍndice == actual):
            barajar_en_su_lugar(genes, secciónPrincipio, 80)
            reglaSeleccionada = next((regla for regla in reglasDeValidación if (genes[regla.Índice] == genes[regla.OtroÍndice])))
        return
    fila = índice_fila(reglaSeleccionada.OtroÍndice)
    principio = (fila * 9)
    índiceA = reglaSeleccionada.OtroÍndice
    índiceB = random.randrange(principio, len(genes))
    (genes[índiceA], genes[índiceB]) = (genes[índiceB], genes[índiceA])
