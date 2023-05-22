from tqdm import tqdm
from matchzoo.data_pack import DataPack
from matchzoo.engine.base_preprocessor import BasePreprocessor
from .chain_transform import chain_transform
from .build_vocab_unit import build_vocab_unit
from . import units


def __init__(self, with_word_hashing: bool=True):
    "\n        DSSM Model preprocessor.\n\n        The word hashing step could eats up a lot of memory. To workaround\n        this problem, set `with_word_hashing` to `False` and use  a\n        :class:`matchzoo.DynamicDataGenerator` with a\n        :class:`matchzoo.preprocessor.units.WordHashing`.\n\n        :param with_word_hashing: Include a word hashing step if `True`.\n\n        Example:\n            >>> import matchzoo as mz\n            >>> train_data = mz.datasets.toy.load_data()\n            >>> test_data = mz.datasets.toy.load_data(stage='test')\n            >>> dssm_preprocessor = mz.preprocessors.DSSMPreprocessor()\n            >>> train_data_processed = dssm_preprocessor.fit_transform(\n            ...     train_data, verbose=0\n            ... )\n            >>> type(train_data_processed)\n            <class 'matchzoo.data_pack.data_pack.DataPack'>\n            >>> test_data_transformed = dssm_preprocessor.transform(test_data,\n            ...                                                     verbose=0)\n            >>> type(test_data_transformed)\n            <class 'matchzoo.data_pack.data_pack.DataPack'>\n\n        "
    super().__init__()
    self._with_word_hashing = with_word_hashing
