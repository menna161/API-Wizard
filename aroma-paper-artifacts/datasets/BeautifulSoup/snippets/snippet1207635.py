from webtest import TestApp as App
from webob import Request
from webob.headers import ResponseHeaders
from bs4 import BeautifulSoup
from jinja2 import Environment, DictLoader
from pydap.lib import walk, __version__
from pydap.handlers.lib import BaseHandler
from pydap.tests.datasets import VerySimpleSequence, SimpleGrid
import unittest
from collections import OrderedDict


def test_body(self):
    'Test the HTML response.\n\n        We use BeautifulSoup to parse the response, and check for some\n        elements that should be there.\n\n        '
    res = self.app.get('/.html')
    soup = BeautifulSoup(res.text, 'html.parser')
    self.assertEqual(soup.title.string, 'Dataset http://localhost/.html')
    self.assertEqual(soup.form['action'], 'http://localhost/.html')
    self.assertEqual(soup.form['method'], 'POST')
    ids = [var.id for var in walk(VerySimpleSequence)]
    for (h2, id_) in zip(soup.find_all('h2'), ids):
        self.assertEqual(h2.string, id_)
