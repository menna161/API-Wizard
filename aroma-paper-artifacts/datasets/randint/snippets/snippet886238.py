import datetime
import random
import unittest
import genetic
from cortadora import *


def test_corta_gira_salta(self):
    anchura = altura = 8
    geneSet = [(lambda : Corta()), (lambda : Gira()), (lambda : Salta(random.randint(0, min(anchura, altura)), random.randint(0, min(anchura, altura))))]
    mínGenes = (anchura * altura)
    máxGenes = int((1.5 * mínGenes))
    rondasMáximasDeMutación = 1
    númeroEsperadoDeInstrucciones = 64

    def fnCrearCampo():
        return CampoToroidal(anchura, altura, ContenidoDelCampo.Hierba)
    self.ejecutar_con(geneSet, anchura, altura, mínGenes, máxGenes, númeroEsperadoDeInstrucciones, rondasMáximasDeMutación, fnCrearCampo, númeroEsperadoDeInstrucciones)
