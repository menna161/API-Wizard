from __future__ import annotations
import datetime
import os
import signal
from dataclasses import dataclass
from enum import Enum
from typing import Any, Dict, List, Optional
import numpy as np
import pandas as pd
import pyarrow as pa
import trino
from trino.dbapi import Cursor
from trino.exceptions import TrinoQueryError
from feast.infra.offline_stores.contrib.trino_offline_store.trino_type_map import trino_to_pa_value_type


def execute(self) -> Results:
    try:
        self.status = QueryStatus.RUNNING
        start_time = datetime.datetime.utcnow()
        self._cursor.execute(operation=self.query_text)
        rows = self._cursor.fetchall()
        end_time = datetime.datetime.utcnow()
        self.execution_time = (end_time - start_time)
        self.status = QueryStatus.COMPLETED
        return Results(data=rows, columns=self._cursor._query.columns)
    except TrinoQueryError as error:
        self.status = QueryStatus.ERROR
        raise error
    finally:
        self.close()
