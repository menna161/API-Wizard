import json
import boto3
from botocore.vendored import requests
import os
from datetime import datetime


def lambda_handler(event, context):
    client = boto3.client('sagemaker')
    print('Calling Sagemaker batch transform')
    try:
        apptime = datetime.now().strftime('%Y-%m-%d-%H-%M-%S')
        response = client.create_transform_job(TransformJobName=(os.environ['transform_job_name'] + apptime), ModelName=os.environ['model_name'], MaxConcurrentTransforms=int(os.environ['max_concurrent']), MaxPayloadInMB=int(os.environ['max_payload_size']), BatchStrategy='MultiRecord', TransformInput={'DataSource': {'S3DataSource': {'S3DataType': 'S3Prefix', 'S3Uri': os.environ['s3_uri_in']}}, 'ContentType': 'text/libsvm', 'CompressionType': 'None', 'SplitType': 'None'}, TransformOutput={'S3OutputPath': os.environ['s3_uri_out']}, TransformResources={'InstanceType': os.environ['instance_type'], 'InstanceCount': int(os.environ['instance_count'])})
        print(response)
        res = {'status': 'Completed', 'name': (os.environ['transform_job_name'] + apptime)}
    except Exception as e:
        res = {'status': 'Failed', 'name': (os.environ['transform_job_name'] + apptime)}
        print(e)
    return res
