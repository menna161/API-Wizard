from crocs.core import printable, RegexOperator, isword, notword, RegexStr, RegexMeta, BadYregex
from random import choice, randint
from itertools import groupby


def __init__(self, *args):
    items = ((RegexStr(ind) if isinstance(ind, str) else ind) for ind in args)
    args = []
    opers = groupby(items, (lambda ind: ind.__class__))
    for (indi, indj) in opers:
        args.extend(indi.reduce_initargs(*indj))
    super(JoinX, self).__init__(*args)
