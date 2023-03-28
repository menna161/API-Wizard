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
def online_write_batch(self, config: RepoConfig, table: FeatureView, data: List[Tuple[(EntityKeyProto, Dict[(str, ValueProto)], datetime, Optional[datetime])]], progress: Optional[Callable[([int], Any)]]) -> None:
    '\n        Writes a batch of feature rows to the online store.\n\n        If a tz-naive timestamp is passed to this method, it is assumed to be UTC.\n\n        Args:\n            config: The config for the current feature store.\n            table: Feature view to which these feature rows correspond.\n            data: A list of quadruplets containing feature data. Each quadruplet contains an entity\n                key, a dict containing feature values, an event timestamp for the row, and the created\n                timestamp for the row if it exists.\n            progress: Function to be called once a batch of rows is written to the online store, used\n                to show progress.\n        '
    pass
