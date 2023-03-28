import os
import uuid
from datetime import datetime
from pathlib import Path
from tempfile import TemporaryFile
from urllib.parse import urlparse
from feast.errors import S3RegistryBucketForbiddenAccess, S3RegistryBucketNotExist
from feast.infra.registry.registry_store import RegistryStore
from feast.protos.feast.core.Registry_pb2 import Registry as RegistryProto
from feast.repo_config import RegistryConfig
from feast.usage import log_exceptions_and_usage
import boto3
from feast.errors import FeastExtrasDependencyImportError
from botocore.exceptions import ClientError
from feast.errors import FeastExtrasDependencyImportError


def _write_registry(self, registry_proto: RegistryProto):
    registry_proto.version_id = str(uuid.uuid4())
    registry_proto.last_updated.FromDatetime(datetime.utcnow())
    file_obj = TemporaryFile()
    file_obj.write(registry_proto.SerializeToString())
    file_obj.seek(0)
    self.s3_client.Bucket(self._bucket).put_object(Body=file_obj, Key=self._key, **self._boto_extra_args)
