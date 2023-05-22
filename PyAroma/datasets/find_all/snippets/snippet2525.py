from __future__ import absolute_import, division, print_function
from bs4 import BeautifulSoup
import pygments
from pygments.lexers import PythonLexer
import requests
from termcolor import colored


def print_ul(ul_element):
    '\n    Prints an unordered list.\n\n    Parameter {bs4.Tag} ul_element: the unordered list to print.\n    '
    for item in ul_element.find_all('li'):
        print(colored(('    - ' + item.text), 'green', attrs=['bold']))
