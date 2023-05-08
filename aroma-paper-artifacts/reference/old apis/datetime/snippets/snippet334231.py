import re
import gflags as flags
from googleapis.codegen import api
from googleapis.codegen import api_library_generator
from googleapis.codegen import cpp_import_manager
from googleapis.codegen import data_types
from googleapis.codegen import language_model
from googleapis.codegen import utilities
from googleapis.codegen.import_definition import ImportDefinition


def _BuildTypeMap(self, options=None):
    'Builds the map of discovery document types to C++ types.\n\n    Args:\n      options: (dict) Code generator options.\n\n    Returns:\n      map of (discovery type, format) keys to (C++ type, import value)\n      values where the import value is header file name to include.\n    '
    self.global_namespace_ = ''
    self.client_namespace_ = 'client'
    builtin_type_h = None
    integral_type_h = '"googleapis/base/integral_types.h"'
    json_type_h = '"googleapis/client/data/jsoncpp_data.h"'
    date_time_h = '"googleapis/client/util/date_time.h"'
    date_h = date_time_h
    self.date_namespace_ = self.client_namespace_
    return {('boolean', None): ('bool', ImportDefinition([builtin_type_h])), ('any', None): ((self.client_namespace_ + '::JsonCppData'), ImportDefinition([json_type_h])), ('integer', None): ('int32', ImportDefinition([integral_type_h])), ('integer', 'int16'): ('int16', ImportDefinition([integral_type_h])), ('integer', 'uint16'): ('uint16', ImportDefinition([integral_type_h])), ('integer', 'int32'): ('int32', ImportDefinition([integral_type_h])), ('integer', 'uint32'): ('uint32', ImportDefinition([integral_type_h])), ('number', None): ('double', ImportDefinition([builtin_type_h])), ('number', 'double'): ('double', ImportDefinition([builtin_type_h])), ('number', 'float'): ('float', ImportDefinition([builtin_type_h])), ('object', None): ((self.client_namespace_ + '::JsonCppData'), ImportDefinition([json_type_h])), ('string', None): ('string', ImportDefinition(['<string>'])), ('string', 'byte'): ('string', ImportDefinition(['<string>'])), ('string', 'date'): ((self.date_namespace_ + '::Date'), ImportDefinition([date_h])), ('string', 'date-time'): ((self.client_namespace_ + '::DateTime'), ImportDefinition([date_time_h])), ('string', 'google-datetime'): ('string', ImportDefinition(['<string>'])), ('string', 'google-duration'): ('string', ImportDefinition(['<string>'])), ('string', 'google-fieldmask'): ('string', ImportDefinition(['<string>'])), ('string', 'int64'): ('int64', ImportDefinition([integral_type_h])), ('string', 'uint64'): ('uint64', ImportDefinition([integral_type_h]))}
