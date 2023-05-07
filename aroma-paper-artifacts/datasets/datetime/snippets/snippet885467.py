import datetime
import random
import unittest
import genetic


def find_knight_positions(self, boardWidth, boardHeight, expectedKnights):
    startTime = datetime.datetime.now()

    def fnDisplay(candidate):
        display(candidate, startTime, boardWidth, boardHeight)

    def fnGetFitness(genes):
        return get_fitness(genes, boardWidth, boardHeight)
    allPositions = [Position(x, y) for y in range(boardHeight) for x in range(boardWidth)]
    if ((boardWidth < 6) or (boardHeight < 6)):
        nonEdgePositions = allPositions
    else:
        nonEdgePositions = [i for i in allPositions if ((0 < i.X < (boardWidth - 1)) and (0 < i.Y < (boardHeight - 1)))]

    def fnGetRandomPosition():
        return random.choice(nonEdgePositions)

    def fnMutate(genes):
        mutate(genes, boardWidth, boardHeight, allPositions, nonEdgePositions)

    def fnCreate():
        return create(fnGetRandomPosition, expectedKnights)
    optimalFitness = (boardWidth * boardHeight)
    best = genetic.get_best(fnGetFitness, None, optimalFitness, None, fnDisplay, fnMutate, fnCreate)
    self.assertTrue((not (optimalFitness > best.Fitness)))
