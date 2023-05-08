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


def _prepare_registry_for_changes(self, project: str):
    'Prepares the Registry for changes by refreshing the cache if necessary.'
    try:
        self._get_registry_proto(project=project, allow_cache=True)
        if (proto_registry_utils.get_project_metadata(self.cached_registry_proto, project) is None):
            self._get_registry_proto(project=project, allow_cache=False)
    except FileNotFoundError:
        registry_proto = RegistryProto()
        registry_proto.registry_schema_version = REGISTRY_SCHEMA_VERSION
        self.cached_registry_proto = registry_proto
        self.cached_registry_proto_created = datetime.utcnow()
    assert self.cached_registry_proto
    if (proto_registry_utils.get_project_metadata(self.cached_registry_proto, project) is None):
        proto_registry_utils.init_project_metadata(self.cached_registry_proto, project)
        self.commit()
    return self.cached_registry_proto
