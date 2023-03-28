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


def _get_registry_proto(self, project: Optional[str], allow_cache: bool=False) -> RegistryProto:
    'Returns the cached or remote registry state\n\n        Args:\n            project: Name of the Feast project (optional)\n            allow_cache: Whether to allow the use of the registry cache when fetching the RegistryProto\n\n        Returns: Returns a RegistryProto object which represents the state of the registry\n        '
    with self._refresh_lock:
        expired = (((self.cached_registry_proto is None) or (self.cached_registry_proto_created is None)) or ((self.cached_registry_proto_ttl.total_seconds() > 0) and (datetime.utcnow() > (self.cached_registry_proto_created + self.cached_registry_proto_ttl))))
        if project:
            old_project_metadata = proto_registry_utils.get_project_metadata(registry_proto=self.cached_registry_proto, project=project)
            if (allow_cache and (not expired) and (old_project_metadata is not None)):
                assert isinstance(self.cached_registry_proto, RegistryProto)
                return self.cached_registry_proto
        elif (allow_cache and (not expired)):
            assert isinstance(self.cached_registry_proto, RegistryProto)
            return self.cached_registry_proto
        registry_proto = self._registry_store.get_registry_proto()
        self.cached_registry_proto = registry_proto
        self.cached_registry_proto_created = datetime.utcnow()
        if (not project):
            return registry_proto
        project_metadata = proto_registry_utils.get_project_metadata(registry_proto=registry_proto, project=project)
        if project_metadata:
            usage.set_current_project_uuid(project_metadata.project_uuid)
        else:
            proto_registry_utils.init_project_metadata(registry_proto, project)
            self.commit()
        return registry_proto
