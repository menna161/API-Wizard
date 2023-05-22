import numpy as np


def frequency_grid_evaluation(self, fmin=0.0, fmax=1.0, fresolution=0.0001):
    ' \n        Computes the selected criterion over a grid of frequencies \n        with limits and resolution specified by the inputs. After that\n        the best local maxima are evaluated over a finer frequency grid\n        \n        Parameters\n        ---------\n        fmin: float\n            starting frequency\n        fmax: float\n            stopping frequency\n        fresolution: float\n            step size in the frequency grid\n        \n        '
    self.freq_step_coarse = fresolution
    freqs = np.arange(start=np.amax([fmin, fresolution]), stop=fmax, step=fresolution, dtype=np.float32)
    (self.per, self.per_single_band) = self._compute_periodogram(freqs)
    self.freq = freqs
