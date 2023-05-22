import datetime
import random
import unittest
import genetic


def barajar_en_su_lugar(genes, primero, último):
    while (primero < último):
        índice = random.randint(primero, último)
        (genes[primero], genes[índice]) = (genes[índice], genes[primero])
        primero += 1
