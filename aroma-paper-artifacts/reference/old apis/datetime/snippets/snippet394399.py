import doctest
import importlib
import pkgutil
import sys
import traceback
import unittest
import feast
from datetime import datetime, timedelta
from feast import Entity, FeatureStore, FeatureView, Field, FileSource
from feast.repo_operations import init_repo
from feast.types import Float32, Int64
import shutil


def setup_feature_store():
    'Prepares the local environment for a FeatureStore docstring test.'
    from datetime import datetime, timedelta
    from feast import Entity, FeatureStore, FeatureView, Field, FileSource
    from feast.repo_operations import init_repo
    from feast.types import Float32, Int64
    init_repo('project', 'local')
    fs = FeatureStore(repo_path='project/feature_repo')
    driver = Entity(name='driver_id', description='driver id')
    driver_hourly_stats = FileSource(path='project/feature_repo/data/driver_stats.parquet', timestamp_field='event_timestamp', created_timestamp_column='created')
    driver_hourly_stats_view = FeatureView(name='driver_hourly_stats', entities=[driver], ttl=timedelta(seconds=(86400 * 1)), schema=[Field(name='conv_rate', dtype=Float32), Field(name='acc_rate', dtype=Float32), Field(name='avg_daily_trips', dtype=Int64)], source=driver_hourly_stats)
    fs.apply([driver_hourly_stats_view, driver])
    fs.materialize(start_date=(datetime.utcnow() - timedelta(hours=3)), end_date=(datetime.utcnow() - timedelta(minutes=10)))
