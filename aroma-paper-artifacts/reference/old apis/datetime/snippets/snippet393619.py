import uuid
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryFile
from urllib.parse import urlparse
from feast.infra.registry.registry_store import RegistryStore
from feast.protos.feast.core.Registry_pb2 import Registry as RegistryProto
from feast.repo_config import RegistryConfig
from feast.usage import log_exceptions_and_usage
import google.cloud.storage as storage
from google.cloud.exceptions import NotFound
from google.cloud.exceptions import NotFound
import google.cloud.storage as storage
from feast.errors import FeastExtrasDependencyImportError


def _write_registry(self, registry_proto: RegistryProto):
    registry_proto.version_id = str(uuid.uuid4())
    registry_proto.last_updated.FromDatetime(datetime.utcnow())
    gs_bucket = self.gcs_client.get_bucket(self._bucket)
    blob = gs_bucket.blob(self._blob)
    file_obj = TemporaryFile()
    file_obj.write(registry_proto.SerializeToString())
    file_obj.seek(0)
    blob.upload_from_file(file_obj)
