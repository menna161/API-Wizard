import unittest
import warnings
import os
import csv
from skosprovider.providers import DictionaryProvider, SimpleCsvProvider
from skosprovider.skos import Concept, Collection, ConceptScheme, Note
from skosprovider.uri import UriPatternGenerator


def test_find_all(self):
    c = trees.find({'type': 'all'})
    self.assertEqual(3, len(c))
