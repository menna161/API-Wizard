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


def test_load_local_data_from_local_with_cache_failed(self):
    with UseModel(self.foo_model, cache_problem=True) as model:
        with self.assertRaises(cherry.exceptions.NotSupportError) as notFoundError:
            res = cherry.base._load_data_from_local(self.foo_model)
        self.assertEqual(str(notFoundError.exception), "Can't load cached data from foo. Please try again after delete cache files.")
