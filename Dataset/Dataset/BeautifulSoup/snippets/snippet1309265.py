import re
from lxml import etree, html
from bs4 import BeautifulSoup, Tag, Comment, ProcessingInstruction, NavigableString, Declaration, Doctype
from html.entities import name2codepoint
from BeautifulSoup import BeautifulSoup, Tag, Comment, ProcessingInstruction, NavigableString, Declaration
from htmlentitydefs import name2codepoint


def _parse(source, beautifulsoup, makeelement, **bsargs):
    if (beautifulsoup is None):
        beautifulsoup = BeautifulSoup
    if hasattr(beautifulsoup, 'HTML_ENTITIES'):
        if ('convertEntities' not in bsargs):
            bsargs['convertEntities'] = 'html'
    if hasattr(beautifulsoup, 'DEFAULT_BUILDER_FEATURES'):
        if ('features' not in bsargs):
            bsargs['features'] = 'html.parser'
    tree = beautifulsoup(source, **bsargs)
    root = _convert_tree(tree, makeelement)
    if ((len(root) == 1) and (root[0].tag == 'html')):
        return root[0]
    root.tag = 'html'
    return root
