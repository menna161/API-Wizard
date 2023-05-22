from __future__ import division, print_function
import numpy as np
from .base_periodogram import BasePeriodogram
from .algorithms.mutual_information import QMI
from .algorithms.string_length import LKSL
from .algorithms.phase_dispersion_minimization import PDM
from .algorithms.analysis_of_variance import AOV
from .algorithms.multiharmonic_aov import MHAOV
from .math import robust_loc, robust_scale
from collections import namedtuple


def _update_periodogram(self, replace_idx, freqs_fine, pers_fine):
    new_best = np.argmax(pers_fine[0])
    if (pers_fine[0][new_best] > self.per[replace_idx]):
        self.freq[replace_idx] = freqs_fine[new_best]
        self.per[replace_idx] = pers_fine[0][new_best]
        for filter_name in self.filter_names:
            self.per_single_band[filter_name][replace_idx] = pers_fine[1][filter_name][new_best]
