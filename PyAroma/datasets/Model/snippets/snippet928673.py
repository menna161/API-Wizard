import os
import shutil
import unittest
import codecs
import pickle
from unittest import mock
import tempfile
import cherry
from collections import namedtuple
from cherry.base import *
from cherry.common import *
from sklearn.feature_extraction.text import CountVectorizer, TfidfVectorizer, HashingVectorizer


@mock.patch('cherry.base.load_files')
def test_load_local_data_from_local_without_cache(self, mock_load_files):
    mock_load_files.return_value = None
    with UseModel(self.foo_model, cache=False) as model:
        res = cherry.base._load_data_from_local(self.foo_model)
        self.assertEqual(res, None)
        mock_load_files.assert_called_once_with(self.foo_model_path, categories=None, encoding=None)
        cache_path = os.path.join(self.foo_model_path, (self.foo_model + '.pkz'))
        self.assertTrue(os.path.exists(cache_path))
