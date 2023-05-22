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


def extract_tables(html):
    soup = BeautifulSoup(html, 'lxml')
    set_ids_by_labels(soup)
    fix_span_tables(soup)
    fix_th(soup)
    remove_ltx_errors(soup)
    flatten_tables(soup)
    tables = soup.find_all('table', class_='ltx_tabular')
    data = []
    for table in tables:
        if (table.find_parent(class_='ltx_authors') is not None):
            continue
        float_div = table.find_parent(is_figure)
        if (float_div and perhaps_not_tabular(table, float_div)):
            continue
        remove_footnotes(table)
        move_out_references(table)
        move_out_text_styles(table)
        move_out_cell_styles(table)
        escape_table_content(table)
        tab = html2data(table)
        if (tab is None):
            continue
        (tab, layout) = fix_table(tab)
        if is_table_empty(tab):
            continue
        caption = None
        if (float_div is not None):
            cap_el = float_div.find('figcaption')
            if (cap_el is not None):
                caption = clear_ws(cap_el.get_text())
        figure_id = table.get('data-figure-id')
        data.append(Table(f'table_{(len(data) + 1):02}', tab, layout.applymap(str), caption, figure_id))
    return data
