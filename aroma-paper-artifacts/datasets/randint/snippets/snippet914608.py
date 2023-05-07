import argparse
import random as R


def r_symbols(size, symbols, length, used=None):
    'Return unique random from given symbols.'
    if ((length == 1) and (not used)):
        return R.sample(symbols, size)
    (rset, used) = (set(), set((used or [])))
    while (len(rset) < size):
        s = r_string(symbols, R.randint(1, length))
        if (s not in used):
            rset.add(s)
    return list(rset)
