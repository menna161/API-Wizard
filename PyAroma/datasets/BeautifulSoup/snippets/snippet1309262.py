import re
from lxml import etree, html
from bs4 import BeautifulSoup, Tag, Comment, ProcessingInstruction, NavigableString, Declaration, Doctype
from html.entities import name2codepoint
from BeautifulSoup import BeautifulSoup, Tag, Comment, ProcessingInstruction, NavigableString, Declaration
from htmlentitydefs import name2codepoint


def fromstring(data, beautifulsoup=None, makeelement=None, **bsargs):
    'Parse a string of HTML data into an Element tree using the\n    BeautifulSoup parser.\n\n    Returns the root ``<html>`` Element of the tree.\n\n    You can pass a different BeautifulSoup parser through the\n    `beautifulsoup` keyword, and a diffent Element factory function\n    through the `makeelement` keyword.  By default, the standard\n    ``BeautifulSoup`` class and the default factory of `lxml.html` are\n    used.\n    '
    return _parse(data, beautifulsoup, makeelement, **bsargs)
