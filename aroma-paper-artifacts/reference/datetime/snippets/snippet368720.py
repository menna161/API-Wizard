import time
from datetime import datetime
from athena_glue_service_logs.partitioners.base_partitioner import BasePartitioner


def test_date_generator(mocker):
    mocker.patch.multiple(BasePartitioner, __abstractmethods__=set())
    base_part = BasePartitioner(s3_location='s3://nowhere')
    today = datetime.utcfromtimestamp(time.time()).date()
    date_tuple = ['2017', '08', '10']
    new_tuples = base_part._get_date_values_since_initial_date(date_tuple)
    assert (new_tuples[0] == ['2017', '08', '11'])
    assert (new_tuples[(- 1)] == today.__str__().split('-'))
