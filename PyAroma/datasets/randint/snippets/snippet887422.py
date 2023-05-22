from crocs.core import printable, RegexOperator, isword, notword, RegexStr, RegexMeta, BadYregex
from random import choice, randint
from itertools import groupby


def invalid_data(self):
    lim = (self.MAX if (self.max == '') else self.max)
    count = randint(self.min, lim)
    data = self.args[0].invalid_data()
    return ''.join((choice(data) for ind in range(count)))
