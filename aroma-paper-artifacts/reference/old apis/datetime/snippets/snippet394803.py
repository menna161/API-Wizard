from datetime import datetime
from typing import Any, Dict, Iterator, Optional, Set
import numpy as np
import pandas as pd
import pyarrow
from pytz import utc
from feast.infra.offline_stores.contrib.trino_offline_store.trino_queries import Trino
from feast.infra.offline_stores.contrib.trino_offline_store.trino_type_map import pa_to_trino_value_type


def format_pandas_row(df: pd.DataFrame) -> str:
    pyarrow_schema = pyarrow_schema_from_dataframe(df=df)

    def _is_nan(value: Any) -> bool:
        if (value is None):
            return True
        try:
            return np.isnan(value)
        except TypeError:
            return False

    def _format_value(row: pd.Series, schema: Dict[(str, Any)]) -> str:
        formated_values = []
        for (row_name, row_value) in row.iteritems():
            if schema[row_name].startswith('timestamp'):
                if isinstance(row_value, datetime):
                    row_value = format_datetime(row_value)
                formated_values.append(f"TIMESTAMP '{row_value}'")
            elif isinstance(row_value, list):
                formated_values.append(f'ARRAY{row_value}')
            elif isinstance(row_value, np.ndarray):
                formated_values.append(f'ARRAY{row_value.tolist()}')
            elif isinstance(row_value, tuple):
                formated_values.append(f'ARRAY{list(row_value)}')
            elif isinstance(row_value, str):
                formated_values.append(f"'{row_value}'")
            elif _is_nan(row_value):
                formated_values.append('NULL')
            else:
                formated_values.append(f'{row_value}')
        return f"({','.join(formated_values)})"
    results = df.apply(_format_value, args=(pyarrow_schema,), axis=1).tolist()
    return ','.join(results)
