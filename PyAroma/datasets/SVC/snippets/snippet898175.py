import chainer
import chainer.functions as F
import numpy as np
from scipy import linalg
from multiprocessing import Pool
from tgan_updater_base import TGANUpdaterBase


def __init__(self, *args, **kwargs):
    self.freq = (kwargs.pop('freq') if ('freq' in kwargs) else 1)
    super(TGANUpdaterWGANSVC, self).__init__(*args, **kwargs)
