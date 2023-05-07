from typing import Optional, Union, Iterable, Iterator, List, IO
from pathlib import Path
from penman.types import Variable, BasicTriple
from penman.tree import Tree
from penman.graph import Graph
from penman.model import Model
from penman._parse import parse, iterparse, parse_triples
from penman._format import format, format_triples
from penman import layout


def __init__(self, model: Model=None):
    if (model is None):
        model = Model()
    self.model = model
