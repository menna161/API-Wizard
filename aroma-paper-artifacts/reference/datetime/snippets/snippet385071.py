import datetime
from boto import dynamodb2
from monocyte.handler import Resource, Handler


def to_string(self, resource):
    table = resource.wrapped
    return ('DynamoDB Table found in {0}, '.format(resource.region) + 'with name {0}, created {1}, with state {2}'.format(table['TableName'], datetime.datetime.fromtimestamp(table['CreationDateTime']).strftime('%Y-%m-%d %H:%M:%S.%f'), table['TableStatus']))
