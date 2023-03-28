from pathlib import Path
import numpy as np
from nnabla.utils.data_source import DataSource


def _get_data(self, position):
    'Return a tuple of data.'
    index = self._indexes[position]
    name = self._waves[index]
    hp = self.hp
    data = np.load(((self._path / 'data') / name))
    (w, label) = (data['wave'], data['speaker_id'])
    w *= (0.99 / (np.max(np.abs(w)) + 1e-07))
    if (len(w) > hp.segment_length):
        idx = self._rng.randint(0, (len(w) - hp.segment_length))
        w = w[idx:(idx + hp.segment_length)]
    else:
        w = np.pad(w, (0, (hp.segment_length - len(w))), mode='constant')
    return (w[(None, ...)], [label])
