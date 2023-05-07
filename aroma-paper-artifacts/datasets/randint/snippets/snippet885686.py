import datetime
import random
import unittest
import genetic
import lawnmower


def test_mow_turn_repeat(self):
    width = height = 8
    geneSet = [(lambda : Mow()), (lambda : Turn()), (lambda : Repeat(random.randint(0, 8), random.randint(0, 8)))]
    minGenes = 3
    maxGenes = 20
    maxMutationRounds = 3
    expectedNumberOfInstructions = 9
    expectedNumberOfSteps = 88

    def fnCreateField():
        return lawnmower.ToroidField(width, height, lawnmower.FieldContents.Grass)
    self.run_with(geneSet, width, height, minGenes, maxGenes, expectedNumberOfInstructions, maxMutationRounds, fnCreateField, expectedNumberOfSteps)
