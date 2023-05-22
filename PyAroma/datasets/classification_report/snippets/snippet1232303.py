import json
from collections import namedtuple
from typing import Generator
import requests
from bs4 import BeautifulSoup


def find_highlighted_idxs(soup, tag='em') -> tuple:
    'Finds indexes of the parts of the soup surrounded by a particular HTML tag\n            relatively to the soup without the tag.\n\n            Example:\n                soup = BeautifulSoup("<em>This</em> is <em>a sample</em> string")\n                tag = "em"\n                Returns: [(0, 4), (8, 16)]\n\n            Args:\n                soup: The BeautifulSoup\'s soup.\n                tag: The HTML tag, which surrounds the parts of the soup.\n\n            Returns:\n                  A list of the tuples, which contain start and end indexes of the soup parts,\n                  surrounded by tags.\n\n            '
    (cur, idxs) = (0, [])
    for t in soup.find_all(text=True):
        if (t.parent.name == tag):
            idxs.append((cur, (cur + len(t))))
        cur += len(t)
    return tuple(idxs)
