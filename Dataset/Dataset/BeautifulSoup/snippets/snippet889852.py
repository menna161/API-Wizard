from bs4 import BeautifulSoup
import pandas as pd
import re
from dataclasses import asdict
from elasticsearch_dsl import Document, Boolean, Object, analyzer, InnerDoc, Keyword, Text, Integer, tokenizer, token_filter, Date
from elasticsearch_dsl.serializer import serializer
from IPython.display import display, Markdown
from elasticsearch_dsl import connections
from axcell.data.doc_utils import get_text, content_in_section, group_content, read_html, put_dummy_anchors, clean_abstract
from .. import config
from pathlib import Path
import sys
from axcell.helpers.jupyter import display_html


@classmethod
def from_html(cls, html, paper_id):
    soup = BeautifulSoup(html, 'html.parser')
    return cls.parse_html(soup, paper_id)
