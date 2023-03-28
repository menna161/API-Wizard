from abc import ABC, abstractmethod
from datetime import datetime
from typing import Any, Callable, Dict, List, Optional, Sequence, Tuple
from feast import Entity
from feast.feature_view import FeatureView
from feast.infra.infra_object import InfraObject
from feast.protos.feast.core.Registry_pb2 import Registry as RegistryProto
from feast.protos.feast.types.EntityKey_pb2 import EntityKey as EntityKeyProto
from feast.protos.feast.types.Value_pb2 import Value as ValueProto
from feast.repo_config import RepoConfig


@abstractmethod
def online_read(self, config: RepoConfig, table: FeatureView, entity_keys: List[EntityKeyProto], requested_features: Optional[List[str]]=None) -> List[Tuple[(Optional[datetime], Optional[Dict[(str, ValueProto)]])]]:
    '\n        Reads features values for the given entity keys.\n\n        Args:\n            config: The config for the current feature store.\n            table: The feature view whose feature values should be read.\n            entity_keys: The list of entity keys for which feature values should be read.\n            requested_features: The list of features that should be read.\n\n        Returns:\n            A list of the same length as entity_keys. Each item in the list is a tuple where the first\n            item is the event timestamp for the row, and the second item is a dict mapping feature names\n            to values, which are returned in proto format.\n        '
    pass
