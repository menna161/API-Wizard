from fastai.text import *
from pathlib import Path
import pandas as pd
import numpy as np
import pickle
from .experiment import Labels, label_map
from .ulmfit_experiment import ULMFiTExperiment
import re
from .ulmfit import ULMFiT_SP
from ...pipeline_logger import pipeline_logger
from copy import deepcopy


@staticmethod
def to_tables(df, transpose=False, n_ulmfit_features=n_ulmfit_features):
    X_tables = []
    Y_tables = []
    ids = []
    C_tables = []
    for (table_id, frame) in df.groupby('table_id'):
        (rows, cols) = ((frame.row.max() + 1), (frame.col.max() + 1))
        x_table = np.zeros((rows, cols, n_features))
        c_table = np.full((rows, cols), '', dtype=np.object)
        for (i, r) in frame.iterrows():
            x_table[(r.row, r.col, :n_ulmfit_features)] = r.features
            c_table[(r.row, r.col)] = r.cell_content
            if (n_layout_features > 0):
                offset = (n_ulmfit_features + n_fasttext_features)
                layout = r.cell_layout
                x_table[(r.row, r.col, offset)] = (1 if (('border-t' in layout) or ('border-tt' in layout)) else (- 1))
                x_table[(r.row, r.col, (offset + 1))] = (1 if (('border-b' in layout) or ('border-bb' in layout)) else (- 1))
                x_table[(r.row, r.col, (offset + 2))] = (1 if (('border-l' in layout) or ('border-ll' in layout)) else (- 1))
                x_table[(r.row, r.col, (offset + 3))] = (1 if (('border-r' in layout) or ('border-rr' in layout)) else (- 1))
                x_table[(r.row, r.col, (offset + 4))] = (1 if (r.cell_reference == 'True') else (- 1))
                x_table[(r.row, r.col, (offset + 5))] = (1 if (r.cell_styles == 'True') else (- 1))
                for (span_idx, span) in enumerate(['cb', 'ci', 'ce', 'rb', 'ri', 're']):
                    x_table[(r.row, r.col, ((offset + 6) + span_idx))] = (1 if (f'span-{span}' in r.cell_layout) else (- 1))
                x_table[(r.row, r.col, (offset + 12))] = (1 if (r.row == 0) else (- 1))
                x_table[(r.row, r.col, (offset + 13))] = (1 if (r.row == (rows - 1)) else (- 1))
                x_table[(r.row, r.col, (offset + 14))] = (1 if (r.col == 0) else (- 1))
                x_table[(r.row, r.col, (offset + 15))] = (1 if (r.col == (cols - 1)) else (- 1))
        X_tables.append(x_table)
        C_tables.append(c_table)
        ids.append(table_id)
        if transpose:
            X_tables.append(x_table.transpose((1, 0, 2)))
            C_tables.append(c_table.transpose())
            ids.append(table_id)
    return (X_tables, C_tables, ids)
