import os
import random
import string
import tempfile
from datetime import datetime, timedelta
import click
import pyarrow as pa
from tqdm import tqdm
from feast import FileSource
from feast.driver_test_data import create_driver_hourly_stats_df
from feast.entity import Entity
from feast.feature_store import FeatureStore
from feast.feature_view import FeatureView
from feast.field import Field
from feast.repo_config import RepoConfig
from feast.types import Float32, Int32
from feast.utils import _convert_arrow_to_proto


@click.command(name='run')
def benchmark_writes():
    project_id = ('test' + ''.join((random.choice((string.ascii_lowercase + string.digits)) for _ in range(10))))
    with tempfile.TemporaryDirectory() as temp_dir:
        store = FeatureStore(config=RepoConfig(registry=os.path.join(temp_dir, 'registry.db'), project=project_id, provider='gcp'))
        parquet_path = os.path.join(temp_dir, 'data.parquet')
        driver = Entity(name='driver_id')
        table = create_driver_hourly_stats_feature_view(create_driver_hourly_stats_source(parquet_path=parquet_path))
        store.apply([table, driver])
        provider = store._get_provider()
        end_date = datetime.utcnow()
        start_date = (end_date - timedelta(days=14))
        customers = list(range(100))
        data = create_driver_hourly_stats_df(customers, start_date, end_date)
        print(data)
        proto_data = _convert_arrow_to_proto(pa.Table.from_pandas(data), table, ['driver_id'])
        with tqdm(total=len(proto_data)) as progress:
            provider.online_write_batch(project=store.project, table=table, data=proto_data, progress=progress.update)
        registry_tables = store.list_feature_views()
        registry_entities = store.list_entities()
        provider.teardown_infra(store.project, tables=registry_tables, entities=registry_entities)
