import inspect
import logging
import time
from datetime import datetime, timedelta
from uuid import uuid4
import botocore
import botocore.session
import pytest
from aws_secretsmanager_caching.config import SecretCacheConfig
from aws_secretsmanager_caching.secret_cache import SecretCache
from botocore.exceptions import ClientError, HTTPClientError, NoCredentialsError


@pytest.fixture(scope='module', autouse=True)
def pre_test_cleanup(self, client):
    logger.info('Starting cleanup operation of previous test secrets...')
    old_secrets = []
    two_days_ago = (datetime.now() - timedelta(days=2))
    paginator = client.get_paginator('list_secrets')
    paginator_config = {'PageSize': 10, 'StartingToken': None}
    iterator = paginator.paginate(PaginationConfig=paginator_config)
    try:
        for page in iterator:
            logger.info('Fetching results from ListSecretValue...')
            for secret in page['SecretList']:
                if (secret['Name'].startswith(TestAwsSecretsManagerCachingInteg.fixture_prefix) and (secret['LastChangedDate'] > two_days_ago) and (secret['LastAccessedDate'] > two_days_ago)):
                    old_secrets.append(secret)
            try:
                paginator_config['StartingToken'] = page['NextToken']
            except KeyError:
                logger.info('reached end of list')
                break
            time.sleep(0.5)
    except ClientError as e:
        logger.error('Got ClientError {0} while calling ListSecrets'.format(e.response['Error']['Code']))
    except HTTPClientError:
        logger.error('Got HTTPClientError while calling ListSecrets')
    except NoCredentialsError:
        logger.fatal('Got NoCredentialsError while calling ListSecrets.')
        raise
    if (len(old_secrets) == 0):
        logger.info('No previously configured test secrets found')
    for secret in old_secrets:
        logger.info('Scheduling deletion of secret {}'.format(secret['Name']))
        try:
            client.delete_secret(SecretId=secret['Name'])
        except ClientError as e:
            logger.error('Got ClientError {0} while calling DeleteSecret for secret {1}'.format(e.response['Error']['Code'], secret['Name']))
        except HTTPClientError:
            logger.error('Got HTTPClientError while calling DeleteSecret for secret {0}'.format(secret['Name']))
        time.sleep(0.5)
    (yield None)
