import pandas as pd
import numpy as np
from functools import wraps
from pathlib import Path
import logging
import warnings
import clr
import System
from System.Data import DataTable
import Microsoft.AnalysisServices.Tabular as AMO
import Microsoft.AnalysisServices.AdomdClient as ADOMD


def _parse_DAX_result(table: 'DataTable') -> pd.DataFrame:
    cols = [c for c in table.Columns.List]
    rows = []
    for r in range(table.Rows.Count):
        row = [table.Rows[r][c] for c in cols]
        rows.append(row)
    df = pd.DataFrame.from_records(rows, columns=[c.ColumnName for c in cols])
    df = df.applymap((lambda x: (np.NaN if isinstance(x, System.DBNull) else x)))
    dt_types = [c.ColumnName for c in cols if (c.DataType.FullName == 'System.DateTime')]
    if dt_types:
        for dtt in dt_types:
            if (not df.loc[(:, dtt)].isna().all()):
                ser = df.loc[(:, dtt)].map((lambda x: x.ToString('s')))
                df.loc[(:, dtt)] = pd.to_datetime(ser)
    types_map = {'System.Int64': int, 'System.Double': float, 'System.String': str}
    col_types = {c.ColumnName: types_map.get(c.DataType.FullName, 'object') for c in cols}
    col_types_ints = {k for (k, v) in col_types.items() if (v == int)}
    ser = df.isna().any(axis=0)
    col_types.update({k: float for k in set(ser[ser].index).intersection(col_types_ints)})
    df = df.astype(col_types)
    return df
