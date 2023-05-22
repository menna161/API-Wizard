import os
from avro import schema
from . import namespace as ns_
from . import logical
import six
import keyword
from avrogen.logical import DEFAULT_LOGICAL_TYPES


def write_preamble(writer, use_logical_types, custom_imports):
    '\n    Writes a preamble of the file containing schema classes\n    :param  writer:\n    :return:\n    '
    writer.write('import json\n')
    writer.write('import os.path\n')
    writer.write('import decimal\n')
    writer.write('import datetime\n')
    writer.write('import six\n')
    for cs in (custom_imports or []):
        writer.write(f'''import {cs}
''')
    writer.write('from avrogen.dict_wrapper import DictWrapper\n')
    writer.write('from avrogen import avrojson\n')
    if use_logical_types:
        writer.write('from avrogen import logical\n')
    writer.write('from avro.schema import RecordSchema, SchemaFromJSONData as make_avsc_object\n')
    writer.write('from avro import schema as avro_schema\n')
    writer.write('from typing import List, Dict, Union, Optional, overload\n')
    writer.write('\n')
