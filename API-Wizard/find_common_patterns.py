"""#Find common patterns - GSPAN"""

import warnings
import os


def common_patterns(trees):
    warnings.filterwarnings('ignore')
    # len_ex = len(dumps)
    minsupport = int(len(trees)*0.5)
    #  -w True
    os.system(
        "python -m gspan_mining -s " + str(minsupport)+" -d True -w True ./input.txt > output.txt")
