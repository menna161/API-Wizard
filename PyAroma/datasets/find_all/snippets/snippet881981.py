import unittest
import warnings
import os
import csv
from skosprovider.providers import DictionaryProvider, SimpleCsvProvider
from skosprovider.skos import Concept, Collection, ConceptScheme, Note
from skosprovider.uri import UriPatternGenerator


def test_find_all_es(self):
    c = trees.find({'label': 'es', 'type': 'all'})
    self.assertEqual(2, len(c))
