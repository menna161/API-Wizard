import datetime
import random
import unittest
import genetic


def display(candidate, startTime):
    timeDiff = (datetime.datetime.now() - startTime)
    for row in range(9):
        line = ' | '.join((' '.join((str(i) for i in candidate.Genes[((row * 9) + i):(((row * 9) + i) + 3)])) for i in [0, 3, 6]))
        print('', line)
        if ((row < 8) and ((row % 3) == 2)):
            print(' ----- + ----- + -----')
    print(' - = -   - = -   - = - {}\t{}\n'.format(candidate.Fitness, timeDiff))
