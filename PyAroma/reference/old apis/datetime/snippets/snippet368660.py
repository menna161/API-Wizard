import logging
from athena_glue_service_logs.catalog_manager import BaseCatalogManager
from athena_glue_service_logs.partitioners.date_partitioner import DatePartitioner
from athena_glue_service_logs.partitioners.null_partitioner import NullPartitioner
from awsglue.transforms import Map


def conversion_actions(self, dynamic_frame):
    from awsglue.transforms import Map

    def combine_datetime(record):
        'Combine two date and time fields into one time field'
        record['time'] = ('%s %s' % (record['date'], record['time']))
        del record['date']
        return record
    mapped_dyf = Map.apply(frame=dynamic_frame, f=combine_datetime)
    return mapped_dyf
