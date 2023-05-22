from bs4 import BeautifulSoup
from collections import UserDict
from datetime import datetime
from dexy.exceptions import InternalDexyProblem
from dexy.exceptions import UserFeedback
from dexy.plugin import TemplatePlugin
from dexy.utils import levenshtein
from dexy.version import DEXY_VERSION
from pygments.styles import get_all_styles
import calendar
import dexy.commands
import dexy.commands.cite
import dexy.data
import dexy.exceptions
import dexy.plugin
import inflection
import inspect
import jinja2
import json
import markdown
import operator
import os
import pygments
import pygments.formatters
import random
import re
import time
import uuid
import xml.etree.ElementTree as ET
import yaml
import yaml
import pprint


def run(self):
    return {'prettify_html': ('Pretty-print HTML using BeautifulSoup', self.prettify_html), 'BeautifulSoup': ('The BeautifulSoup module.', BeautifulSoup)}
