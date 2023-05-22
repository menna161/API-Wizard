import datetime
import random
import unittest
import genetic
from cortadora import *


def test_corta_gira_repite(self):
    anchura = altura = 8
    geneSet = [(lambda : Corta()), (lambda : Gira()), (lambda : Repite(random.randint(0, 8), random.randint(0, 8)))]
    mínGenes = 3
    máxGenes = 20
    rondasMáximasDeMutación = 3
    númeroEsperadoDeInstrucciones = 9
    númeroEsperadoDePasos = 88

    def fnCrearCampo():
        return CampoToroidal(anchura, altura, ContenidoDelCampo.Hierba)
    self.ejecutar_con(geneSet, anchura, altura, mínGenes, máxGenes, númeroEsperadoDeInstrucciones, rondasMáximasDeMutación, fnCrearCampo, númeroEsperadoDePasos)
