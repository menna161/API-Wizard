import time
from datetime import datetime, timedelta
from athena_glue_service_logs.partitioners.grouped_date_partitioner import GroupedDatePartitioner
from utils import S3Stubber


def test_partition_scanner(mocker):
    date_part = GroupedDatePartitioner(s3_location='s3://nowhere/some_logs')
    today = datetime.utcfromtimestamp(time.time()).date()
    s3_stub = S3Stubber('list_objects_v2')
    s3_stub.add_response(response_with_prefixes(), delimiter_request())
    for i in range(2):
        s3_stub.add_response(response_for_objects(region_s3_keys()[i]), prefix_request(response_with_prefixes()['CommonPrefixes'][i]['Prefix']))
    with mocker.patch('boto3.client', return_value=s3_stub.client):
        with s3_stub.stubber:
            new_tuples = date_part.build_partitions_from_s3()
    assert (new_tuples[0] == ['us-west-2', '2017', '08', '11'])
    assert (new_tuples[(- 1)] == (['us-east-1'] + today.__str__().split('-')))
