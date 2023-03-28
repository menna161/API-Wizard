from datetime import datetime, timedelta
from tempfile import mkstemp
import pytest
from pytest_lazyfixture import lazy_fixture
from feast import BatchFeatureView
from feast.aggregation import Aggregation
from feast.data_format import AvroFormat, ParquetFormat
from feast.data_source import KafkaSource
from feast.entity import Entity
from feast.feature_store import FeatureStore
from feast.feature_view import FeatureView
from feast.field import Field
from feast.infra.offline_stores.file_source import FileSource
from feast.infra.online_stores.sqlite import SqliteOnlineStoreConfig
from feast.repo_config import RepoConfig
from feast.stream_feature_view import stream_feature_view
from feast.types import Array, Bytes, Float32, Int64, String
from tests.utils.cli_repo_creator import CliRunner, get_example_repo
from tests.utils.data_source_test_creator import prep_file_source
import pandas as pd
import pandas as pd


@pytest.mark.parametrize('test_feature_store', [lazy_fixture('feature_store_with_local_registry')])
@pytest.mark.parametrize('dataframe_source', [lazy_fixture('simple_dataset_1')])
def test_reapply_feature_view(test_feature_store, dataframe_source):
    with prep_file_source(df=dataframe_source, timestamp_field='ts_1') as file_source:
        e = Entity(name='id', join_keys=['id_join_key'])
        fv1 = FeatureView(name='my_feature_view_1', schema=[Field(name='string_col', dtype=String)], entities=[e], source=file_source, ttl=timedelta(minutes=5))
        test_feature_store.apply([fv1, e])
        fv_stored = test_feature_store.get_feature_view(fv1.name)
        assert (len(fv_stored.materialization_intervals) == 0)
        test_feature_store.materialize(datetime(2020, 1, 1), datetime(2021, 1, 1))
        fv_stored = test_feature_store.get_feature_view(fv1.name)
        assert (len(fv_stored.materialization_intervals) == 1)
        test_feature_store.apply([fv1])
        fv_stored = test_feature_store.get_feature_view(fv1.name)
        assert (len(fv_stored.materialization_intervals) == 1)
        fv1 = FeatureView(name='my_feature_view_1', schema=[Field(name='int64_col', dtype=Int64)], entities=[e], source=file_source, ttl=timedelta(minutes=5))
        test_feature_store.apply([fv1])
        fv_stored = test_feature_store.get_feature_view(fv1.name)
        assert (len(fv_stored.materialization_intervals) == 0)
        test_feature_store.teardown()
