from athena_glue_service_logs.catalog_manager import BaseCatalogManager
from athena_glue_service_logs.partitioners.date_partitioner import DatePartitioner
from athena_glue_service_logs.partitioners.null_partitioner import NullPartitioner
from awsglue.transforms import Map
from dateutil import parser


def conversion_actions(self, dynamic_frame):
    from awsglue.transforms import Map
    from dateutil import parser

    def combine_datetime(record):
        "Parse the funky timestamp because python doesn't support %z"
        parsed_timestamp = parser.parse(record['time'].replace(':', ' ', 1))
        record['time'] = parsed_timestamp.isoformat()
        return record
    mapped_dyf = Map.apply(frame=dynamic_frame, f=combine_datetime)
    return mapped_dyf
