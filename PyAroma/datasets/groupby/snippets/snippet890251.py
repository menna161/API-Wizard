import dataclasses
from dataclasses import dataclass
import json
from pathlib import Path
import numpy as np
import pandas as pd
from axcell.models.structure.nbsvm import *
from sklearn.metrics import confusion_matrix
from matplotlib import pyplot as plt
import seaborn as sn
from enum import Enum
import pickle


def _transform_df(self, df):
    df.cell_reference = (df.cell_reference != '').astype(str)
    df.cell_styles = df.cell_styles.astype(str)
    if (self.merge_type not in ['concat', 'vote_maj', 'vote_avg', 'vote_max']):
        raise Exception(f'merge_type must be one of concat, vote_maj, vote_avg, vote_max, but {self.merge_type} was given')
    if (self.mark_this_paper and ((self.merge_type != 'concat') or self.this_paper)):
        raise Exception("merge_type must be 'concat' and this_paper must be false")
    if (self.evidence_limit is not None):
        df = df.groupby(by=['ext_id', 'this_paper']).head(self.evidence_limit)
    if (self.context_tokens is not None):
        df.loc['text_highlited'] = df['text_highlited'].apply(self._limit_context)
        df.loc['text'] = df['text_highlited'].str.replace('<b>', ' ').replace('</b>', ' ')
    if (self.evidence_source != 'text'):
        df = df.copy(True)
        if self.mask:
            df['text'] = df[self.evidence_source].replace(re.compile('<b>.*?</b>'), ' xxmask ')
        else:
            df['text'] = df[self.evidence_source]
    elif self.mask:
        raise Exception("Masking with evidence_source='text' makes no sense")
    duplicates_columns = ['text', 'cell_content', 'cell_type', 'row_context', 'col_context', 'cell_reference', 'cell_layout', 'cell_styles']
    columns_to_keep = ['ext_id', 'cell_content', 'cell_type', 'row_context', 'col_context', 'cell_reference', 'cell_layout', 'cell_styles']
    if self.mark_this_paper:
        df = df.groupby(by=(columns_to_keep + ['this_paper'])).text.apply((lambda x: '\n'.join(x.values))).reset_index()
        this_paper_map = {True: 'this paper', False: 'other paper'}
        df.text = ((('xxfld 3 ' + df.this_paper.apply(this_paper_map.get)) + ' ') + df.text)
        df = df.groupby(by=columns_to_keep).text.apply((lambda x: ' '.join(x.values))).reset_index()
    elif (not self.fixed_this_paper):
        if (self.merge_fragments and (self.merge_type == 'concat')):
            df = df.groupby(by=(columns_to_keep + ['this_paper'])).text.apply((lambda x: '\n'.join(x.values))).reset_index()
        if self.drop_duplicates:
            df = df.drop_duplicates(duplicates_columns).fillna('')
        if self.this_paper:
            df = df[df.this_paper]
    else:
        if self.this_paper:
            df = df[df.this_paper]
        if (self.merge_fragments and (self.merge_type == 'concat')):
            df = df.groupby(by=columns_to_keep).text.apply((lambda x: '\n'.join(x.values))).reset_index()
        if self.drop_duplicates:
            df = df.drop_duplicates(duplicates_columns).fillna('')
    if self.split_btags:
        df['text'] = df['text'].replace(re.compile('(\\</?b\\>)'), ' \\1 ')
    df = df.replace(re.compile('(xxref|xxanchor)-[\\w\\d-]*'), '\\1 ')
    if self.remove_num:
        df = df.replace(re.compile('(^|[ ])\\d+\\.\\d+(\\b|%)'), ' xxnum ')
        df = df.replace(re.compile('(^|[ ])\\d+(\\b|%)'), ' xxnum ')
    df = df.replace(re.compile('\\bdata set\\b'), ' dataset ')
    df['label'] = df['cell_type'].apply((lambda x: label_map.get(x, 0)))
    if (not self.distinguish_model_source):
        df['label'] = df['label'].apply((lambda x: (x if (x != Labels.COMPETING_MODEL.value) else Labels.PAPER_MODEL.value)))
    df['label'] = pd.Categorical(df['label'])
    return df
