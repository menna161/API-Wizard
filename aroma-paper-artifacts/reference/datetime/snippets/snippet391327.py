from __future__ import print_function, unicode_literals, division, absolute_import
import sys
import collections
import json
import os
import re
import csv
import dxpy
from ..utils.printing import fill
from ..bindings import DXRecord
from ..bindings.dxdataobject_functions import is_dxlink
from ..bindings.dxfile import DXFile
from ..utils.resolver import resolve_existing_path, is_hashid, ResolutionError
from ..utils.file_handle import as_handle
from ..exceptions import err_exit, PermissionDenied, InvalidInput, InvalidState
import pandas as pd


def create_entity_dframe(self, entity, is_primary_entity, global_primary_key):
    '\n            Returns DataDictionary pandas DataFrame for an entity.\n        '
    required_columns = ['entity', 'name', 'type', 'primary_key_type']
    extra_cols = ['coding_name', 'concept', 'description', 'folder_path', 'is_multi_select', 'is_sparse_coding', 'linkout', 'longitudinal_axis_type', 'referenced_entity_field', 'relationship', 'title', 'units']
    dataset_datatype_dict = {'integer': 'integer', 'double': 'float', 'date': 'date', 'datetime': 'datetime', 'string': 'string'}
    dcols = {col: [] for col in (required_columns + extra_cols)}
    dcols['entity'] = ([entity['name']] * len(entity['fields']))
    dcols['referenced_entity_field'] = ([''] * len(entity['fields']))
    dcols['relationship'] = ([''] * len(entity['fields']))
    for field in entity['fields']:
        field_dict = entity['fields'][field]
        dcols['name'].append(field_dict['name'])
        dcols['type'].append(dataset_datatype_dict[field_dict['type']])
        dcols['primary_key_type'].append((('global' if is_primary_entity else 'local') if (entity['primary_key'] and (field_dict['name'] == entity['primary_key'])) else ''))
        dcols['coding_name'].append((field_dict['coding_name'] if field_dict['coding_name'] else ''))
        dcols['concept'].append(field_dict['concept'])
        dcols['description'].append(field_dict['description'])
        dcols['folder_path'].append((' > '.join(field_dict['folder_path']) if (('folder_path' in field_dict.keys()) and field_dict['folder_path']) else ''))
        dcols['is_multi_select'].append(('yes' if field_dict['is_multi_select'] else ''))
        dcols['is_sparse_coding'].append(('yes' if field_dict['is_sparse_coding'] else ''))
        dcols['linkout'].append(field_dict['linkout'])
        dcols['longitudinal_axis_type'].append((field_dict['longitudinal_axis_type'] if field_dict['longitudinal_axis_type'] else ''))
        dcols['title'].append(field_dict['title'])
        dcols['units'].append(field_dict['units'])
    try:
        dframe = pd.DataFrame(dcols)
    except ValueError as exc:
        raise exc
    return dframe
