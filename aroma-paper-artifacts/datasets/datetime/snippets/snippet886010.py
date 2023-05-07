import datetime
import random
import unittest
import genetic


def encontrarCaballoPosiciones(self, tableroAncho, tableroAltura, caballosEsperados):
    horaInicio = datetime.datetime.now()

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio, tableroAncho, tableroAltura)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes, tableroAncho, tableroAltura)
    todasPosiciones = [Posición(x, y) for y in range(tableroAltura) for x in range(tableroAncho)]
    if ((tableroAncho < 6) or (tableroAltura < 6)):
        posicionesNoBordeadas = todasPosiciones
    else:
        posicionesNoBordeadas = [i for i in todasPosiciones if ((0 < i.X < (tableroAncho - 1)) and (0 < i.Y < (tableroAltura - 1)))]

    def fnObtenerPosiciónAleatoria():
        return random.choice(posicionesNoBordeadas)

    def fnMutar(genes):
        mutar(genes, tableroAncho, tableroAltura, todasPosiciones, posicionesNoBordeadas)

    def fnCrear():
        return crear(fnObtenerPosiciónAleatoria, caballosEsperados)
    aptitudÓptima = (tableroAncho * tableroAltura)
    mejor = genetic.obtener_mejor(fnObtenerAptitud, None, aptitudÓptima, None, fnMostrar, fnMutar, fnCrear)
    self.assertTrue((not (aptitudÓptima > mejor.Aptitud)))
