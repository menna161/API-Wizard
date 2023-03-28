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
def plan(self, desired_repo_contents: RepoContents) -> Tuple[(RegistryDiff, InfraDiff, Infra)]:
    'Dry-run registering objects to metadata store.\n\n        The plan method dry-runs registering one or more definitions (e.g., Entity, FeatureView), and produces\n        a list of all the changes the that would be introduced in the feature repo. The changes computed by the plan\n        command are for informational purposes, and are not actually applied to the registry.\n\n        Args:\n            desired_repo_contents: The desired repo state.\n\n        Raises:\n            ValueError: The \'objects\' parameter could not be parsed properly.\n\n        Examples:\n            Generate a plan adding an Entity and a FeatureView.\n\n            >>> from feast import FeatureStore, Entity, FeatureView, Feature, FileSource, RepoConfig\n            >>> from feast.feature_store import RepoContents\n            >>> from datetime import timedelta\n            >>> fs = FeatureStore(repo_path="project/feature_repo")\n            >>> driver = Entity(name="driver_id", description="driver id")\n            >>> driver_hourly_stats = FileSource(\n            ...     path="project/feature_repo/data/driver_stats.parquet",\n            ...     timestamp_field="event_timestamp",\n            ...     created_timestamp_column="created",\n            ... )\n            >>> driver_hourly_stats_view = FeatureView(\n            ...     name="driver_hourly_stats",\n            ...     entities=[driver],\n            ...     ttl=timedelta(seconds=86400 * 1),\n            ...     source=driver_hourly_stats,\n            ... )\n            >>> registry_diff, infra_diff, new_infra = fs.plan(RepoContents(\n            ...     data_sources=[driver_hourly_stats],\n            ...     feature_views=[driver_hourly_stats_view],\n            ...     on_demand_feature_views=list(),\n            ...     stream_feature_views=list(),\n            ...     request_feature_views=list(),\n            ...     entities=[driver],\n            ...     feature_services=list())) # register entity and feature view\n        '
    self._validate_all_feature_views(desired_repo_contents.feature_views, desired_repo_contents.on_demand_feature_views, desired_repo_contents.request_feature_views, desired_repo_contents.stream_feature_views)
    _validate_data_sources(desired_repo_contents.data_sources)
    self._make_inferences(desired_repo_contents.data_sources, desired_repo_contents.entities, desired_repo_contents.feature_views, desired_repo_contents.on_demand_feature_views, desired_repo_contents.stream_feature_views, desired_repo_contents.feature_services)
    registry_diff = diff_between(self._registry, self.project, desired_repo_contents)
    self._registry.refresh(project=self.project)
    current_infra_proto = self._registry.proto().infra.__deepcopy__()
    desired_registry_proto = desired_repo_contents.to_registry_proto()
    new_infra = self._provider.plan_infra(self.config, desired_registry_proto)
    new_infra_proto = new_infra.to_proto()
    infra_diff = diff_infra_protos(current_infra_proto, new_infra_proto)
    return (registry_diff, infra_diff, new_infra)
