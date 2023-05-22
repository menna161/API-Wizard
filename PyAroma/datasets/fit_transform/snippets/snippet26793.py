import abc
import functools
import typing
from pathlib import Path
import dill
import matchzoo as mz


def fit_transform(self, data_pack: 'mz.DataPack', verbose: int=1) -> 'mz.DataPack':
    '\n        Call fit-transform.\n\n        :param data_pack: :class:`DataPack` object to be processed.\n        :param verbose: Verbosity.\n        '
    return self.fit(data_pack, verbose=verbose).transform(data_pack, verbose=verbose)
