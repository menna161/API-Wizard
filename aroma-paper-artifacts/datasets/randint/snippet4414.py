import random
import string
import types
import typing
import math
import itertools
from abc import ABC, abstractmethod
from collections import Counter
from math import factorial
import sys


def render(self, **kwargs):
    cnt = 1
    if (self.start > (- 1)):
        cnt = StringGenerator.randomizer.randint(self.start, self.cnt)
    else:
        cnt = self.cnt
    return ''.join((self.chars[StringGenerator.randomizer.randint(0, (len(self.chars) - 1))] for x in range(cnt)))
