import datetime
import random
import unittest
import genetic
import lawnmower


def test_mow_turn_jump_validating(self):
    width = height = 8
    geneSet = [(lambda : Mow()), (lambda : Turn()), (lambda : Jump(random.randint(0, min(width, height)), random.randint(0, min(width, height))))]
    minGenes = (width * height)
    maxGenes = int((1.5 * minGenes))
    maxMutationRounds = 3
    expectedNumberOfInstructions = 79

    def fnCreateField():
        return lawnmower.ValidatingField(width, height, lawnmower.FieldContents.Grass)
    self.run_with(geneSet, width, height, minGenes, maxGenes, expectedNumberOfInstructions, maxMutationRounds, fnCreateField, expectedNumberOfInstructions)
