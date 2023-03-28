import time
from datetime import datetime, timedelta
from athena_glue_service_logs.partitioners.date_partitioner import DatePartitioner
from utils import S3Stubber


def test_partition_scanner(mocker):
    date_part = DatePartitioner(s3_location='s3://nowhere')
    today = datetime.utcfromtimestamp(time.time()).date()
    s3_stub = S3Stubber.for_single_request('list_objects_v2', request_params(), [basic_s3_key()])
    with mocker.patch('boto3.client', return_value=s3_stub.client):
        with s3_stub.stubber:
            new_tuples = date_part.build_partitions_from_s3()
    assert (new_tuples[0] == ['2017', '08', '11'])
    assert (new_tuples[(- 1)] == today.__str__().split('-'))
