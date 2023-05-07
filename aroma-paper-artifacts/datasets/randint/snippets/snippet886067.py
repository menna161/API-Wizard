import datetime
import random
import sys
import unittest
import genetic


def mutar(genes, artículos, pesoMáximo, volumenMáximo, ventana):
    ventana.deslizar()
    aptitud = obtener_aptitud(genes)
    pesoRestante = (pesoMáximo - aptitud.PesoTotal)
    volumenRestante = (volumenMáximo - aptitud.VolumenTotal)
    eliminando = ((len(genes) > 1) and (random.randint(0, 10) == 0))
    if eliminando:
        índice = random.randrange(0, len(genes))
        ac = genes[índice]
        artículo = ac.Artículo
        pesoRestante += (artículo.Peso * ac.Cantidad)
        volumenRestante += (artículo.Volumen * ac.Cantidad)
        del genes[índice]
    añadiendo = (((pesoRestante > 0) or (volumenRestante > 0)) and ((len(genes) == 0) or ((len(genes) < len(artículos)) and (random.randint(0, 100) == 0))))
    if añadiendo:
        nuevoGen = añadir(genes, artículos, pesoRestante, volumenRestante)
        if (nuevoGen is not None):
            genes.append(nuevoGen)
            return
    índice = random.randrange(0, len(genes))
    ac = genes[índice]
    artículo = ac.Artículo
    pesoRestante += (artículo.Peso * ac.Cantidad)
    volumenRestante += (artículo.Volumen * ac.Cantidad)
    artículoACambiar = ((len(genes) < len(artículos)) and (random.randint(0, 4) == 0))
    if artículoACambiar:
        artículoÍndice = artículos.index(ac.Artículo)
        principio = max(1, (artículoÍndice - ventana.Tamaño))
        fin = min((len(artículos) - 1), (artículoÍndice + ventana.Tamaño))
        artículo = artículos[random.randint(principio, fin)]
    cantidadMáxima = cantidad_máxima(artículo, pesoRestante, volumenRestante)
    if (cantidadMáxima > 0):
        genes[índice] = ArtículoCantidad(artículo, (cantidadMáxima if (ventana.Tamaño > 1) else random.randint(1, cantidadMáxima)))
    else:
        del genes[índice]
