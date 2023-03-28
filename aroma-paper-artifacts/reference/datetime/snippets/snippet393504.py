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
def validate_logged_features(self, source: FeatureService, start: datetime, end: datetime, reference: ValidationReference, throw_exception: bool=True, cache_profile: bool=True) -> Optional[ValidationFailed]:
    '\n        Load logged features from an offline store and validate them against provided validation reference.\n\n        Args:\n            source: Logs source object (currently only feature services are supported)\n            start: lower bound for loading logged features\n            end:  upper bound for loading logged features\n            reference: validation reference\n            throw_exception: throw exception or return it as a result\n            cache_profile: store cached profile in Feast registry\n\n        Returns:\n            Throw or return (depends on parameter) ValidationFailed exception if validation was not successful\n            or None if successful.\n\n        '
    if (not flags_helper.is_test()):
        warnings.warn('Logged features validation is an experimental feature. This API is unstable and it could and most probably will be changed in the future. We do not guarantee that future changes will maintain backward compatibility.', RuntimeWarning)
    if (not isinstance(source, FeatureService)):
        raise ValueError('Only feature service is currently supported as a source')
    j = self._get_provider().retrieve_feature_service_logs(feature_service=source, start_date=start, end_date=end, config=self.config, registry=self.registry)
    try:
        t = j.to_arrow(validation_reference=reference)
    except ValidationFailed as exc:
        if throw_exception:
            raise
        return exc
    else:
        print(f'{t.shape[0]} rows were validated.')
    if cache_profile:
        self.apply(reference)
    return None
