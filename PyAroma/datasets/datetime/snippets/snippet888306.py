import datetime
import logging
import os
import boto3


def get_metrics(timestamp):
    queue = os.environ['QueueName']
    group = os.environ['GroupName']
    response = CW.get_metric_data(StartTime=timestamp, EndTime=(timestamp + datetime.timedelta(minutes=5)), ScanBy='TimestampAscending', MetricDataQueries=[{'Id': 'maxANOMV', 'MetricStat': {'Metric': {'Namespace': 'AWS/SQS', 'MetricName': 'ApproximateNumberOfMessagesVisible', 'Dimensions': [{'Name': 'QueueName', 'Value': f'{queue}'}]}, 'Period': 300, 'Stat': 'Maximum', 'Unit': 'Count'}}, {'Id': 'sumNOER', 'MetricStat': {'Metric': {'Namespace': 'AWS/SQS', 'MetricName': 'NumberOfEmptyReceives', 'Dimensions': [{'Name': 'QueueName', 'Value': f'{queue}'}]}, 'Period': 300, 'Stat': 'Sum', 'Unit': 'Count'}}, {'Id': 'avgGISI', 'MetricStat': {'Metric': {'Namespace': 'AWS/AutoScaling', 'MetricName': 'GroupInServiceInstances', 'Dimensions': [{'Name': 'AutoScalingGroupName', 'Value': f'{group}'}]}, 'Period': 300, 'Stat': 'Average', 'Unit': 'None'}}])
    return {m['Id']: dict(zip(m['Timestamps'], m['Values']))[timestamp] for m in response['MetricDataResults']}
