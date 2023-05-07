import datetime
import unittest
import genetic


def color(self, file, colores):
    (reglas, nodos) = cargar_datos(file)
    valorÓptimo = len(reglas)
    búsquedaDeColor = {color[0]: color for color in colores}
    geneSet = list(búsquedaDeColor.keys())
    horaInicio = datetime.datetime.now()
    búsquedaDeÍndiceDeNodo = {key: índice for (índice, key) in enumerate(sorted(nodos))}

    def fnMostrar(candidato):
        mostrar(candidato, horaInicio)

    def fnObtenerAptitud(genes):
        return obtener_aptitud(genes, reglas, búsquedaDeÍndiceDeNodo)
    mejor = genetic.obtener_mejor(fnObtenerAptitud, len(nodos), valorÓptimo, geneSet, fnMostrar)
    self.assertTrue((not (valorÓptimo > mejor.Aptitud)))
    llaves = sorted(nodos)
    for índice in range(len(nodos)):
        print(((llaves[índice] + ' es ') + búsquedaDeColor[mejor.Genes[índice]]))
