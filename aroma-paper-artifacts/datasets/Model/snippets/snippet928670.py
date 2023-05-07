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


@mock.patch('cherry.base._load_data_from_local')
def test_load_data_found(self, mock_load_files):
    with UseModel(self.foo_model) as model:
        load_data(self.foo_model)
    mock_load_files.assert_called_once_with(self.foo_model, categories=None, encoding=None)
