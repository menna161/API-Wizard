import json
from abc import ABC, abstractmethod
from collections import defaultdict
from datetime import datetime
from typing import Any, Dict, List, Optional
from google.protobuf.json_format import MessageToJson
from proto import Message
from feast.base_feature_view import BaseFeatureView
from feast.data_source import DataSource
from feast.entity import Entity
from feast.feature_service import FeatureService
from feast.feature_view import FeatureView
from feast.infra.infra_object import Infra
from feast.on_demand_feature_view import OnDemandFeatureView
from feast.project_metadata import ProjectMetadata
from feast.protos.feast.core.Registry_pb2 import Registry as RegistryProto
from feast.request_feature_view import RequestFeatureView
from feast.saved_dataset import SavedDataset, ValidationReference
from feast.stream_feature_view import StreamFeatureView


@abstractmethod
def apply_materialization(self, feature_view: FeatureView, project: str, start_date: datetime, end_date: datetime, commit: bool=True):
    '\n        Updates materialization intervals tracked for a single feature view in Feast\n\n        Args:\n            feature_view: Feature view that will be updated with an additional materialization interval tracked\n            project: Feast project that this feature view belongs to\n            start_date (datetime): Start date of the materialization interval to track\n            end_date (datetime): End date of the materialization interval to track\n            commit: Whether the change should be persisted immediately\n        '
