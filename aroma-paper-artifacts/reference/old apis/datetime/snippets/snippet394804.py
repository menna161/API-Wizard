from datetime import datetime
from typing import Any, Dict, Iterator, Optional, Set
import numpy as np
import pandas as pd
import pyarrow
from pytz import utc
from feast.infra.offline_stores.contrib.trino_offline_store.trino_queries import Trino
from feast.infra.offline_stores.contrib.trino_offline_store.trino_type_map import pa_to_trino_value_type


def format_datetime(t: datetime) -> str:
    if t.tzinfo:
        t = t.astimezone(tz=utc)
    return t.strftime('%Y-%m-%d %H:%M:%S.%f')
