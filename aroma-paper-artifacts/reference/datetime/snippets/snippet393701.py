import base64
import json
import logging
from concurrent.futures import ThreadPoolExecutor, wait
from dataclasses import dataclass
from datetime import datetime
from typing import Callable, List, Literal, Optional, Sequence, Union
import boto3
from pydantic import StrictStr
from tqdm import tqdm
from feast import utils
from feast.batch_feature_view import BatchFeatureView
from feast.constants import FEATURE_STORE_YAML_ENV_NAME
from feast.entity import Entity
from feast.feature_view import FeatureView
from feast.infra.materialization.batch_materialization_engine import BatchMaterializationEngine, MaterializationJob, MaterializationJobStatus, MaterializationTask
from feast.infra.offline_stores.offline_store import OfflineStore
from feast.infra.online_stores.online_store import OnlineStore
from feast.infra.registry.base_registry import BaseRegistry
from feast.repo_config import FeastConfigBaseModel, RepoConfig
from feast.stream_feature_view import StreamFeatureView
from feast.utils import _get_column_names
from feast.version import get_version


def _materialize_one(self, registry: BaseRegistry, feature_view: Union[(BatchFeatureView, StreamFeatureView, FeatureView)], start_date: datetime, end_date: datetime, project: str, tqdm_builder: Callable[([int], tqdm)]):
    entities = []
    for entity_name in feature_view.entities:
        entities.append(registry.get_entity(entity_name, project))
    (join_key_columns, feature_name_columns, timestamp_field, created_timestamp_column) = _get_column_names(feature_view, entities)
    job_id = f'{feature_view.name}-{start_date}-{end_date}'
    offline_job = self.offline_store.pull_latest_from_table_or_query(config=self.repo_config, data_source=feature_view.batch_source, join_key_columns=join_key_columns, feature_name_columns=feature_name_columns, timestamp_field=timestamp_field, created_timestamp_column=created_timestamp_column, start_date=start_date, end_date=end_date)
    paths = offline_job.to_remote_storage()
    max_workers = (len(paths) if (len(paths) <= 20) else 20)
    executor = ThreadPoolExecutor(max_workers=max_workers)
    futures = []
    for path in paths:
        payload = {FEATURE_STORE_YAML_ENV_NAME: self.feature_store_base64, 'view_name': feature_view.name, 'view_type': 'batch', 'path': path}
        logger.info('Invoking materialization for %s', path)
        futures.append(executor.submit(self.lambda_client.invoke, FunctionName=self.lambda_name, InvocationType='RequestResponse', Payload=json.dumps(payload)))
    (done, not_done) = wait(futures)
    logger.info('Done: %s Not Done: %s', done, not_done)
    for f in done:
        response = f.result()
        output = json.loads(response['Payload'].read())
        logger.info(f"Ingested task; request id {response['ResponseMetadata']['RequestId']}, Output: {output}")
    for f in not_done:
        response = f.result()
        logger.error(f'Ingestion failed: {response}')
    return LambdaMaterializationJob(job_id=job_id, status=(MaterializationJobStatus.SUCCEEDED if (not not_done) else MaterializationJobStatus.ERROR))
