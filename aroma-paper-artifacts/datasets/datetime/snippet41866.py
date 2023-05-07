from django.utils import text, timezone
from faker.generator import random
from .compat import HAS_GEOS, HAS_PSYCOPG2
from django.contrib.gis import gdal, geos
from psycopg2.extras import DateRange, DateTimeTZRange, NumericRange
from .field_mappings import mappings_types
from .values import Evaluator


def daterange(faker, field, *args, **kwargs):
    lower = faker.date_time().date()
    upper = faker.date_time_between_dates(datetime_start=lower).date()
    return DateRange(lower, upper)
