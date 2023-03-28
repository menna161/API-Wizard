import os, sys, copy, random, torch, numpy as np
from collections import OrderedDict, defaultdict


def random(self):
    return random.randint(0, (len(self.meta_archs) - 1))
