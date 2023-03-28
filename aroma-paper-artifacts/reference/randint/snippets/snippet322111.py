import random, string, itertools, traceback
from more_itertools import peekable
from ananas import PineappleBot, reply, html_strip_tags


def perform_roll(dice=1, sides=6, keep=(- 1), drop=(- 1)):
    r = []
    rolls = []
    if (sides == 0):
        raise SillyDiceError("I don't have any zero-dimensional constructs but when I find one, I'll get back to you.")
    if (dice > 50):
        raise SillyDiceError("I don't have that many dice!")
    if (sides > 1000):
        raise SillyDiceError('I rolled the sphere and it rolled off the table.')
    for i in range(dice):
        roll = random.randint(1, sides)
        r.append(roll)
        rolls.append((i, roll))
    rolls.sort(key=(lambda roll: (- roll[1])))
    if (keep > 0):
        rolls = rolls[0:keep]
    elif ((drop > 0) and (drop < dice)):
        rolls = rolls[0:(- drop)]
    elif ((drop == (- 1)) and (keep == (- 1))):
        pass
    else:
        raise SillyDiceError('Whoops, dropped all the dice')
    if (len(rolls) < len(r)):
        r = [roll for (i, roll) in enumerate(r) if ((i, roll) in rolls)]
    return r
