import datetime
import random
import unittest
import genetic


def mutar(genes, tableroAncho, tableroAltura, todasPosiciones, posicionesNoBordeadas):
    cuenta = (2 if (random.randint(0, 10) == 0) else 1)
    while (cuenta > 0):
        cuenta -= 1
        posiciónACaballoÍndices = dict(((p, []) for p in todasPosiciones))
        for (i, caballo) in enumerate(genes):
            for posición in obtener_ataques(caballo, tableroAncho, tableroAltura):
                posiciónACaballoÍndices[posición].append(i)
        caballoÍndices = set((i for i in range(len(genes))))
        noAtacados = []
        for kvp in posiciónACaballoÍndices.items():
            if (len(kvp[1]) > 1):
                continue
            if (len(kvp[1]) == 0):
                noAtacados.append(kvp[0])
                continue
            for p in kvp[1]:
                if (p in caballoÍndices):
                    caballoÍndices.remove(p)
        posicionesPotenciales = ([p for posiciones in map((lambda x: obtener_ataques(x, tableroAncho, tableroAltura)), noAtacados) for p in posiciones if (p in posicionesNoBordeadas)] if (len(noAtacados) > 0) else posicionesNoBordeadas)
        índiceDeGen = (random.randrange(0, len(genes)) if (len(caballoÍndices) == 0) else random.choice([i for i in caballoÍndices]))
        posición = random.choice(posicionesPotenciales)
        genes[índiceDeGen] = posición
