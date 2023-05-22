import datetime
import random
import unittest
import genetic
from cortadora import *


def test_corta_gira_salta_validando(self):
    anchura = altura = 8
    geneSet = [(lambda : Corta()), (lambda : Gira()), (lambda : Salta(random.randint(0, min(anchura, altura)), random.randint(0, min(anchura, altura))))]
    mínGenes = (anchura * altura)
    máxGenes = int((1.5 * mínGenes))
    rondasMáximasDeMutación = 3
    númeroEsperadoDeInstrucciones = 79

    def fnCrearCampo():
        return CampoValidando(anchura, altura, ContenidoDelCampo.Hierba)
    self.ejecutar_con(geneSet, anchura, altura, mínGenes, máxGenes, númeroEsperadoDeInstrucciones, rondasMáximasDeMutación, fnCrearCampo, númeroEsperadoDeInstrucciones)
