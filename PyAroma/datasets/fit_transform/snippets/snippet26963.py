from tqdm import tqdm
from . import units
from .chain_transform import chain_transform
from matchzoo import DataPack
from matchzoo.engine.base_preprocessor import BasePreprocessor
from .build_vocab_unit import built_bert_vocab_unit
from .build_unit_from_data_pack import build_unit_from_data_pack


def __init__(self, bert_vocab_path: str, fixed_length_left: int=30, fixed_length_right: int=30, filter_mode: str='df', filter_low_freq: float=2, filter_high_freq: float=float('inf'), remove_stop_words: bool=False, lower_case: bool=True, chinese_version: bool=False):
    "\n        Bert-base Model preprocessor.\n\n        Example:\n            >>> import matchzoo as mz\n            >>> train_data = mz.datasets.toy.load_data()\n            >>> test_data = mz.datasets.toy.load_data(stage='test')\n            >>> # The argument 'bert_vocab_path' must feed the bert vocab path\n            >>> bert_preprocessor = mz.preprocessors.BertPreprocessor(\n            ...     bert_vocab_path=\n            ...     'matchzoo/datasets/bert_resources/uncased_vocab_100.txt')\n            >>> train_data_processed = bert_preprocessor.fit_transform(\n            ...     train_data)\n            >>> test_data_processed = bert_preprocessor.transform(test_data)\n\n        "
    super().__init__()
    self._fixed_length_left = fixed_length_left
    self._fixed_length_right = fixed_length_right
    self._bert_vocab_path = bert_vocab_path
    self._left_fixedlength_unit = units.FixedLength(self._fixed_length_left, pad_mode='post')
    self._right_fixedlength_unit = units.FixedLength(self._fixed_length_right, pad_mode='post')
    self._filter_unit = units.FrequencyFilter(low=filter_low_freq, high=filter_high_freq, mode=filter_mode)
    self._units = self._default_units()
    self._vocab_unit = built_bert_vocab_unit(self._bert_vocab_path)
    if chinese_version:
        self._units.insert(1, units.ChineseTokenize())
    if lower_case:
        self._units.append(units.Lowercase())
        self._units.append(units.StripAccent())
    self._units.append(units.WordPieceTokenize(self._vocab_unit.state['term_index']))
    if remove_stop_words:
        self._units.append(units.StopRemoval())
