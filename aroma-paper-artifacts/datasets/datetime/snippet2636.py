import datetime
import re
import secrets
import boto3


@state_function('Initialize')
def initialize(state, uid):
    orig_db = rds_client.describe_db_instances(DBInstanceIdentifier=state['db_identifier'])['DBInstances'][0]
    state['engine'] = orig_db['Engine']
    state['temp_snapshot_id'] = ((state['db_identifier'][:55] + '-') + secrets.token_hex(5))
    state['temp_snapshot_id2'] = ((state['db_identifier'][:55] + '-') + secrets.token_hex(5))
    state['temp_db_id'] = ((state['db_identifier'][:55] + '-') + secrets.token_hex(5))
    state['target_snapshot_id'] = ((state['db_identifier'][:55] + '-') + secrets.token_hex(5))
    tsid = state['target_snapshot_id'] = state['snapshot_format'].format(database_identifier=state['db_identifier'], date=datetime.datetime.now())
    if ((not re.match('[a-z][a-z0-9\\-]{1,62}', tsid, re.I)) or ('--' in tsid) or (tsid[(- 1)] == '-')):
        raise ValueError(f'Invalid snapshot id generated from format - {tsid}')
    if (state['kms'] and (orig_db['DBInstanceClass'] in ['db.m1.small', 'db.m1.medium', 'db.m1.large', 'db.m1.xlarge', 'db.m2.xlarge', 'db.m2.2xlarge', 'db.m2.4xlarge', 'db.t2.micro'])):
        raise ValueError("Instance type doesn't support encryption.")
