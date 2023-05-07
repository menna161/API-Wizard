import datetime
import random
import unittest
import genetic
import lawnmower


def test_mow_turn_jump_func(self):
    width = height = 8
    geneSet = [(lambda : Mow()), (lambda : Turn()), (lambda : Jump(random.randint(0, min(width, height)), random.randint(0, min(width, height)))), (lambda : Func())]
    minGenes = 3
    maxGenes = 20
    maxMutationRounds = 3
    expectedNumberOfInstructions = 18
    expectedNumberOfSteps = 65

    def fnCreateField():
        return lawnmower.ToroidField(width, height, lawnmower.FieldContents.Grass)
    self.run_with(geneSet, width, height, minGenes, maxGenes, expectedNumberOfInstructions, maxMutationRounds, fnCreateField, expectedNumberOfSteps)
