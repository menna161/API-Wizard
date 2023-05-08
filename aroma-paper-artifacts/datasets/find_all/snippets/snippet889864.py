import sys
from bs4 import BeautifulSoup, Comment, NavigableString
import fire
from pathlib import Path
import pandas as pd
import numpy as np
import json
import re
from ast import literal_eval
from collections import OrderedDict
from dataclasses import dataclass
from typing import Set
from axcell.data.table import Table


def escape_table_content(soup):
    for item in soup.find_all(['td', 'th']):
        escaped = escape(clear_ws(item.get_text()))
        item.string = escaped
