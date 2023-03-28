from types import MethodType
from typing import List, Optional
import pandas as pd
from pyspark.sql import DataFrame, SparkSession
from pyspark.sql.avro.functions import from_avro
from pyspark.sql.functions import col, from_json
from feast.data_format import AvroFormat, JsonFormat
from feast.data_source import KafkaSource, PushMode
from feast.feature_store import FeatureStore
from feast.infra.contrib.stream_processor import ProcessorConfig, StreamProcessor, StreamTable
from feast.stream_feature_view import StreamFeatureView


def batch_write(row: DataFrame, batch_id: int):
    rows: pd.DataFrame = row.toPandas()
    rows = rows.sort_values(by=(self.join_keys + [self.sfv.timestamp_field]), ascending=True).groupby(self.join_keys).nth(0)
    rows['created'] = pd.to_datetime('now', utc=True)
    rows = rows.reset_index()
    if self.preprocess_fn:
        rows = self.preprocess_fn(rows)
    if (rows.size > 0):
        if ((to == PushMode.ONLINE) or (to == PushMode.ONLINE_AND_OFFLINE)):
            self.fs.write_to_online_store(self.sfv.name, rows)
        if ((to == PushMode.OFFLINE) or (to == PushMode.ONLINE_AND_OFFLINE)):
            self.fs.write_to_offline_store(self.sfv.name, rows)
