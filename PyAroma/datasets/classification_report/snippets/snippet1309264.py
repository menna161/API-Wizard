import re
from lxml import etree, html
from bs4 import BeautifulSoup, Tag, Comment, ProcessingInstruction, NavigableString, Declaration, Doctype
from html.entities import name2codepoint
from BeautifulSoup import BeautifulSoup, Tag, Comment, ProcessingInstruction, NavigableString, Declaration
from htmlentitydefs import name2codepoint


def convert_tree(beautiful_soup_tree, makeelement=None):
    'Convert a BeautifulSoup tree to a list of Element trees.\n\n    Returns a list instead of a single root Element to support\n    HTML-like soup with more than one root element.\n\n    You can pass a different Element factory through the `makeelement`\n    keyword.\n    '
    root = _convert_tree(beautiful_soup_tree, makeelement)
    children = root.getchildren()
    for child in children:
        root.remove(child)
    return children
