import numpy as np


def finetune_best_frequencies(self, fresolution=1e-05, n_local_optima=10):
    '\n        Computes the selected criterion over a grid of frequencies \n        around a specified amount of  local optima of the periodograms. This\n        function is intended for additional fine tuning of the results obtained\n        with grid_search\n        '
    local_optima_index = self.find_local_maxima(n_local_optima)
    for local_optimum_index in local_optima_index:
        fmin = (self.freq[local_optimum_index] - self.freq_step_coarse)
        fmax = (self.freq[local_optimum_index] + self.freq_step_coarse)
        freqs_fine = np.arange(fmin, fmax, step=fresolution, dtype=np.float32)
        pers_fine = self._compute_periodogram(freqs_fine)
        self._update_periodogram(local_optimum_index, freqs_fine, pers_fine)
    idx = np.argsort(self.per[local_optima_index])[::(- 1)]
    if (n_local_optima > 0):
        self.best_local_optima = local_optima_index[idx]
    else:
        self.best_local_optima = local_optima_index
