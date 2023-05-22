import datetime
import random
import unittest
import genetic


def mutate(genes, boardWidth, boardHeight, allPositions, nonEdgePositions):
    count = (2 if (random.randint(0, 10) == 0) else 1)
    while (count > 0):
        count -= 1
        positionToKnightIndexes = dict(((p, []) for p in allPositions))
        for (i, knight) in enumerate(genes):
            for position in get_attacks(knight, boardWidth, boardHeight):
                positionToKnightIndexes[position].append(i)
        knightIndexes = set((i for i in range(len(genes))))
        unattacked = []
        for kvp in positionToKnightIndexes.items():
            if (len(kvp[1]) > 1):
                continue
            if (len(kvp[1]) == 0):
                unattacked.append(kvp[0])
                continue
            for p in kvp[1]:
                if (p in knightIndexes):
                    knightIndexes.remove(p)
        potentialKnightPositions = ([p for positions in map((lambda x: get_attacks(x, boardWidth, boardHeight)), unattacked) for p in positions if (p in nonEdgePositions)] if (len(unattacked) > 0) else nonEdgePositions)
        geneIndex = (random.randrange(0, len(genes)) if (len(knightIndexes) == 0) else random.choice([i for i in knightIndexes]))
        position = random.choice(potentialKnightPositions)
        genes[geneIndex] = position
