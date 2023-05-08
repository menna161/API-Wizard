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
def parse_html(cls, soup, paper_id):
    put_dummy_anchors(soup)
    abstract = soup.select('div.ltx_abstract')
    author = soup.select('div.ltx_authors')
    p = cls(title=get_text(soup.title), authors=get_text(*author), abstract=clean_abstract(get_text(*abstract)), meta={'id': paper_id})
    for el in (abstract + author):
        el.extract()
    fragments = Fragments()
    doc = soup.find('article')
    if doc:
        footnotes = doc.select('.ltx_role_footnote > .ltx_note_outer')
        for ft in footnotes:
            ft.extract()
        idx = 0
        for (idx, idx2, section_header, content) in group_content(doc):
            content = content.strip()
            if ((p.abstract == '') and ('abstract' in section_header.lower())):
                p.abstract = clean_abstract(content)
            else:
                order = (((idx + 1) * 1000) + idx2)
                f = Fragment(paper_id=paper_id, order=order, header=section_header, text=content, meta={'id': f'{paper_id}-{order}'})
                fragments.append(f)
        idx += 1
        idx2 = 0
        for ft in footnotes:
            order = (((idx + 1) * 1000) + idx2)
            f = Fragment(paper_id=paper_id, order=order, header='xxanchor-footnotes Footnotes', text=get_text(ft), meta={'id': f'{paper_id}-{order}'})
            fragments.append(f)
            idx2 += 1
    else:
        print(f'No article found for {paper_id}', file=sys.stderr)
    p.fragments = fragments
    return p
