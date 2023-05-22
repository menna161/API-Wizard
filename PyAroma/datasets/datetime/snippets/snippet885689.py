import datetime
import random
import unittest
import genetic
import lawnmower


def run_with(self, geneSet, width, height, minGenes, maxGenes, expectedNumberOfInstructions, maxMutationRounds, fnCreateField, expectedNumberOfSteps):
    mowerStartLocation = lawnmower.Location(int((width / 2)), int((height / 2)))
    mowerStartDirection = lawnmower.Directions.South.value

    def fnCreate():
        return create(geneSet, 1, height)

    def fnEvaluate(instructions):
        program = Program(instructions)
        mower = lawnmower.Mower(mowerStartLocation, mowerStartDirection)
        field = fnCreateField()
        try:
            program.evaluate(mower, field)
        except RecursionError:
            pass
        return (field, mower, program)

    def fnGetFitness(genes):
        return get_fitness(genes, fnEvaluate)
    startTime = datetime.datetime.now()

    def fnDisplay(candidate):
        display(candidate, startTime, fnEvaluate)

    def fnMutate(child):
        mutate(child, geneSet, minGenes, maxGenes, fnGetFitness, maxMutationRounds)
    optimalFitness = Fitness((width * height), expectedNumberOfInstructions, expectedNumberOfSteps)
    best = genetic.get_best(fnGetFitness, None, optimalFitness, None, fnDisplay, fnMutate, fnCreate, maxAge=None, poolSize=10, crossover=crossover)
    self.assertTrue((not (optimalFitness > best.Fitness)))
