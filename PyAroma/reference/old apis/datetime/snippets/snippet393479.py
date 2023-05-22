import copy
import itertools
import os
import warnings
from collections import Counter, defaultdict
from datetime import datetime, timedelta
from pathlib import Path
from typing import TYPE_CHECKING, Any, Callable, Dict, Iterable, List, Mapping, Optional, Sequence, Set, Tuple, Union, cast
import pandas as pd
import pyarrow as pa
from colorama import Fore, Style
from google.protobuf.timestamp_pb2 import Timestamp
from tqdm import tqdm
from feast import feature_server, flags_helper, ui_server, utils
from feast.base_feature_view import BaseFeatureView
from feast.batch_feature_view import BatchFeatureView
from feast.data_source import DataSource, KafkaSource, KinesisSource, PushMode, PushSource
from feast.diff.infra_diff import InfraDiff, diff_infra_protos
from feast.diff.registry_diff import RegistryDiff, apply_diff_to_registry, diff_between
from feast.dqm.errors import ValidationFailed
from feast.entity import Entity
from feast.errors import DataSourceRepeatNamesException, EntityNotFoundException, FeatureNameCollisionError, FeatureViewNotFoundException, PushSourceNotFoundException, RequestDataNotFoundInEntityDfException, RequestDataNotFoundInEntityRowsException
from feast.feast_object import FeastObject
from feast.feature_service import FeatureService
from feast.feature_view import DUMMY_ENTITY, DUMMY_ENTITY_ID, DUMMY_ENTITY_NAME, DUMMY_ENTITY_VAL, FeatureView
from feast.inference import update_data_sources_with_inferred_event_timestamp_col, update_feature_views_with_inferred_features_and_entities
from feast.infra.infra_object import Infra
from feast.infra.provider import Provider, RetrievalJob, get_provider
from feast.infra.registry.base_registry import BaseRegistry
from feast.infra.registry.registry import Registry
from feast.infra.registry.sql import SqlRegistry
from feast.on_demand_feature_view import OnDemandFeatureView
from feast.online_response import OnlineResponse
from feast.protos.feast.serving.ServingService_pb2 import FieldStatus, GetOnlineFeaturesResponse
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import RepeatedValue, Value
from feast.repo_config import RepoConfig, load_repo_config
from feast.repo_contents import RepoContents
from feast.request_feature_view import RequestFeatureView
from feast.saved_dataset import SavedDataset, SavedDatasetStorage, ValidationReference
from feast.stream_feature_view import StreamFeatureView
from feast.type_map import feast_value_type_to_python_type, python_values_to_proto_values
from feast.usage import log_exceptions, log_exceptions_and_usage, set_usage_attribute
from feast.value_type import ValueType
from feast.version import get_version
from feast.embedded_go.online_features_service import EmbeddedOnlineFeatureServer
from feast.data_source import PushSource
from feast.embedded_go.online_features_service import EmbeddedOnlineFeatureServer
from feast import transformation_server


@log_exceptions_and_usage
def materialize(self, start_date: datetime, end_date: datetime, feature_views: Optional[List[str]]=None) -> None:
    '\n        Materialize data from the offline store into the online store.\n\n        This method loads feature data in the specified interval from either\n        the specified feature views, or all feature views if none are specified,\n        into the online store where it is available for online serving.\n\n        Args:\n            start_date (datetime): Start date for time range of data to materialize into the online store\n            end_date (datetime): End date for time range of data to materialize into the online store\n            feature_views (List[str]): Optional list of feature view names. If selected, will only run\n                materialization for the specified feature views.\n\n        Examples:\n            Materialize all features into the online store over the interval\n            from 3 hours ago to 10 minutes ago.\n            >>> from feast import FeatureStore, RepoConfig\n            >>> from datetime import datetime, timedelta\n            >>> fs = FeatureStore(repo_path="project/feature_repo")\n            >>> fs.materialize(\n            ...     start_date=datetime.utcnow() - timedelta(hours=3), end_date=datetime.utcnow() - timedelta(minutes=10)\n            ... )\n            Materializing...\n            <BLANKLINE>\n            ...\n        '
    if (utils.make_tzaware(start_date) > utils.make_tzaware(end_date)):
        raise ValueError(f'The given start_date {start_date} is greater than the given end_date {end_date}.')
    feature_views_to_materialize = self._get_feature_views_to_materialize(feature_views)
    _print_materialization_log(start_date, end_date, len(feature_views_to_materialize), self.config.online_store.type)
    for feature_view in feature_views_to_materialize:
        provider = self._get_provider()
        print(f'{(Style.BRIGHT + Fore.GREEN)}{feature_view.name}{Style.RESET_ALL}:')

        def tqdm_builder(length):
            return tqdm(total=length, ncols=100)
        start_date = utils.make_tzaware(start_date)
        end_date = utils.make_tzaware(end_date)
        provider.materialize_single_feature_view(config=self.config, feature_view=feature_view, start_date=start_date, end_date=end_date, registry=self._registry, project=self.project, tqdm_builder=tqdm_builder)
        self._registry.apply_materialization(feature_view, self.project, start_date, end_date)
