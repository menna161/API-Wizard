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
    today = datetime.today()
    month = today.month
    year = today.year
    cal = calendar.Calendar()
    caldates = list(cal.itermonthdates(year, month))
    return {'datetime': ('The Python datetime module.', datetime), 'calendar': ('A Calendar instance from Python calendar module.', calendar), 'caldates': ('List of calendar dates in current month.', caldates), 'cal': ('Shortcut for `calendar`.', calendar), 'today': ('Result of datetime.today().', today), 'month': ('Current month.', month), 'year': ('Current year.', year)}
