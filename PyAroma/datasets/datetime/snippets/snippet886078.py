import datetime
import random
import sys
import unittest
import genetic


def rellenar_mochila(self, artículos, pesoMáximo, volumenMáximo, aptitudÓptima):
    horaInicio = datetime.datetime.now()
    ventana = Ventana(1, max(1, int((len(artículos) / 3))), int((len(artículos) / 2)))
    artículosOrdenados = sorted(artículos, key=(lambda artículo: artículo.Valor))

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes)

    def fnCrear():
        return crear(artículos, pesoMáximo, volumenMáximo)

    def fnMutar(genes):
        mutar(genes, artículosOrdenados, pesoMáximo, volumenMáximo, ventana)
    mejor = genetic.obtener_mejor(fnObtenerAptitud, None, aptitudÓptima, None, fnMostrar, fnMutar, fnCrear, edadMáxima=50)
    self.assertTrue((not (aptitudÓptima > mejor.Aptitud)))
