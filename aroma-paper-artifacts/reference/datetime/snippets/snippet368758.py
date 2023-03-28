import time
from datetime import datetime, timedelta
from athena_glue_service_logs.partitioners.grouped_date_partitioner import GroupedDatePartitioner
from utils import S3Stubber


def test_find_new_partitions(mocker):
    date_part = GroupedDatePartitioner(s3_location='s3://nowhere')
    today = datetime.utcfromtimestamp(time.time()).date()
    yesterday = (today - timedelta(days=1))
    existing_part = (['us-west-2'] + yesterday.__str__().split('-'))
    s3_stub = S3Stubber.for_single_request('list_objects_v2', today_objects_request(), today_objects())
    with mocker.patch('boto3.client', return_value=s3_stub.client):
        with s3_stub.stubber:
            new_partitions = date_part.find_recent_partitions([existing_part])
    assert (len(new_partitions) == 1)
    assert (new_partitions == [(['us-west-2'] + today.__str__().split('-'))])
