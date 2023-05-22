import logging
from datetime import datetime, timedelta
from enum import Enum
from pathlib import Path
from threading import Lock
from typing import Any, Dict, List, Optional
from urllib.parse import urlparse
from google.protobuf.internal.containers import RepeatedCompositeFieldContainer
from proto import Message
from feast import usage
from feast.base_feature_view import BaseFeatureView
from feast.data_source import DataSource
from feast.entity import Entity
from feast.errors import ConflictingFeatureViewNames, DataSourceNotFoundException, EntityNotFoundException, FeatureServiceNotFoundException, FeatureViewNotFoundException, ValidationReferenceNotFound
from feast.feature_service import FeatureService
from feast.feature_view import FeatureView
from feast.importer import import_class
from feast.infra.infra_object import Infra
from feast.infra.registry import proto_registry_utils
from feast.infra.registry.base_registry import BaseRegistry
from feast.infra.registry.registry_store import NoopRegistryStore
from feast.on_demand_feature_view import OnDemandFeatureView
from feast.project_metadata import ProjectMetadata
from feast.protos.feast.core.Registry_pb2 import Registry as RegistryProto
from feast.repo_config import RegistryConfig
from feast.repo_contents import RepoContents
from feast.request_feature_view import RequestFeatureView
from feast.saved_dataset import SavedDataset, ValidationReference
from feast.stream_feature_view import StreamFeatureView
from feast.infra.registry.sql import SqlRegistry


def apply_saved_dataset(self, saved_dataset: SavedDataset, project: str, commit: bool=True):
    now = datetime.utcnow()
    if (not saved_dataset.created_timestamp):
        saved_dataset.created_timestamp = now
    saved_dataset.last_updated_timestamp = now
    saved_dataset_proto = saved_dataset.to_proto()
    saved_dataset_proto.spec.project = project
    self._prepare_registry_for_changes(project)
    assert self.cached_registry_proto
    for (idx, existing_saved_dataset_proto) in enumerate(self.cached_registry_proto.saved_datasets):
        if ((existing_saved_dataset_proto.spec.name == saved_dataset_proto.spec.name) and (existing_saved_dataset_proto.spec.project == project)):
            del self.cached_registry_proto.saved_datasets[idx]
            break
    self.cached_registry_proto.saved_datasets.append(saved_dataset_proto)
    if commit:
        self.commit()
