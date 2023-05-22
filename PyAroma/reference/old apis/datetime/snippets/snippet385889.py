import datetime
import json
from boto3.dynamodb.types import TypeDeserializer


def default(self, obj):
    if hasattr(obj, 'attribute_values'):
        return obj.attribute_values
    elif isinstance(obj, datetime.datetime):
        return obj.isoformat()
    return json.JSONEncoder.default(self, obj)
