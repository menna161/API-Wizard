import re
from lxml import etree, html
from bs4 import BeautifulSoup, Tag, Comment, ProcessingInstruction, NavigableString, Declaration, Doctype
from html.entities import name2codepoint
from BeautifulSoup import BeautifulSoup, Tag, Comment, ProcessingInstruction, NavigableString, Declaration
from htmlentitydefs import name2codepoint


def parse(file, beautifulsoup=None, makeelement=None, **bsargs):
    'Parse a file into an ElemenTree using the BeautifulSoup parser.\n\n    You can pass a different BeautifulSoup parser through the\n    `beautifulsoup` keyword, and a diffent Element factory function\n    through the `makeelement` keyword.  By default, the standard\n    ``BeautifulSoup`` class and the default factory of `lxml.html` are\n    used.\n    '
    if (not hasattr(file, 'read')):
        file = open(file)
    root = _parse(file, beautifulsoup, makeelement, **bsargs)
    return etree.ElementTree(root)
