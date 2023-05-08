import adage
import adage.dagstate
from adage import adagetask, adageop, Rule
import random
import logging
import time


@adagetask
def variableoutput():
    log.info('determining number of pdf jobs to launch')
    pdfjobs = random.randint(1, 2)
    time.sleep((2 + (10 * random.random())))
    return pdfjobs
