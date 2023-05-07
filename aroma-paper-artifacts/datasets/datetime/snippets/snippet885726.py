import datetime
import random
import unittest
import circuits
import genetic


def display(candidate, startTime):
    circuit = nodes_to_circuit(candidate.Genes)[0]
    timeDiff = (datetime.datetime.now() - startTime)
    print('{}\t{}\t{}'.format(circuit, candidate.Fitness, timeDiff))
