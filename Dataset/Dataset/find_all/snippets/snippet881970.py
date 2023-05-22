import unittest
import warnings
import os
import csv
from skosprovider.providers import DictionaryProvider, SimpleCsvProvider
from skosprovider.skos import Concept, Collection, ConceptScheme, Note
from skosprovider.uri import UriPatternGenerator


def test_find_all_sort(self):
    c = trees.find({'type': 'all'}, sort='id', sort_order='desc')
    self.assertEqual([3, '2', '1'], [cc['id'] for cc in c])
    c = trees.find({'type': 'all'}, sort='sortlabel', sort_order='asc')
    self.assertEqual([3, '1', '2'], [cc['id'] for cc in c])
    c = trees.find({'type': 'all'}, sort='sortlabel', sort_order='desc')
    self.assertEqual(['2', '1', 3], [cc['id'] for cc in c])
