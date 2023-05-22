import datetime
import random
import unittest
import genetic
from cortadora import *


def test_corta_gira_salta_func(self):
    anchura = altura = 8
    geneSet = [(lambda : Corta()), (lambda : Gira()), (lambda : Salta(random.randint(0, min(anchura, altura)), random.randint(0, min(anchura, altura)))), (lambda : Func())]
    mínGenes = 3
    máxGenes = 20
    rondasMáximasDeMutación = 3
    númeroEsperadoDeInstrucciones = 17
    númeroEsperadoDePasos = 64

    def fnCrearCampo():
        return CampoToroidal(anchura, altura, ContenidoDelCampo.Hierba)
    self.ejecutar_con(geneSet, anchura, altura, mínGenes, máxGenes, númeroEsperadoDeInstrucciones, rondasMáximasDeMutación, fnCrearCampo, númeroEsperadoDePasos)
