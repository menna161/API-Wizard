from crocs.core import printable, RegexOperator, isword, notword, RegexStr, RegexMeta, BadYregex
from random import choice, randint
from itertools import groupby


def valid_data(self):
    lim = ((self.MAX + self.min) if (self.max == '') else self.max)
    count = randint(self.min, lim)
    data = (self.args[0].valid_data() for ind in range(0, count))
    data = ''.join(data)
    return data
