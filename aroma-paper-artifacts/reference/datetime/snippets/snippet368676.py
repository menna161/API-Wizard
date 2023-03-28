import time
from datetime import datetime, timedelta
from athena_glue_service_logs.partitioners.base_partitioner import BasePartitioner
from athena_glue_service_logs.utils import S3Reader


def find_recent_partitions(self, existing_partitions):
    partitions_to_add = []
    today = datetime.utcfromtimestamp(time.time()).date()
    day_diff = 0
    for _ in range(self.MAX_RECENT_DAYS):
        new_day = (today + timedelta(days=day_diff))
        new_day_tuple = new_day.strftime('%Y-%m-%d').split('-')
        if ((not existing_partitions) or (existing_partitions[(- 1)] != new_day_tuple)):
            if S3Reader(self.build_partitioned_path(new_day_tuple)).does_have_objects():
                partitions_to_add.append(new_day_tuple)
        else:
            break
        day_diff -= 1
    return partitions_to_add
