import datetime
import json
import re
from collections import OrderedDict
from pathlib import Path
from typing import Any, Dict, List, Optional, Union
from tomlkit import loads


def parse_toml_file(filepath: Union[(str, Path)]) -> Any:
    'Parse TOML config file.\n\n    Parameters\n    ----------\n    filepath\n        The file name or path to the TOML file.\n\n    Returns\n    -------\n    date_time : datetime.datetime\n    header : list\n    block_names : list\n    (variables, values, comments, blocks) : Tuple[str, Any, str, str]\n    '
    from tomlkit import loads
    with open(filepath, 'r') as fp:
        toml_dict = loads(fp.read())
    blocks = list()
    variables = list()
    values = list()
    comments = list()
    header = None
    date_time = None
    for (key, item) in toml_dict.items():
        if (key in ['__header__', 'header']):
            header = item
        elif (key in ['__datetime__', 'datetime']):
            date_time = item
        else:
            for (var, val) in item.items():
                if isinstance(val, str):
                    if re.fullmatch('\\d\\d\\d:\\d\\d', val):
                        val = val.split(':')
                        val = datetime.timedelta(hours=int(val[0]), minutes=int(val[1]))
                variables.append(var)
                values.append(val)
                blocks.append(key)
    variable_comment = dict()
    for key in toml_dict.keys():
        lines = toml_dict[key].as_string().split('\n')
        while ('' in lines):
            lines.remove('')
        comment = list()
        for line in lines:
            if line.startswith('#'):
                comment.append(line[2:])
            else:
                variable_comment[line.split('=')[0].strip()] = '\n'.join(comment)
                comment = list()
    for var in variables:
        if (var in variable_comment):
            comments.append(variable_comment[var])
        else:
            comments.append('')
    block_names = list(toml_dict.keys())
    try:
        block_names.remove('__header__')
    except ValueError:
        pass
    try:
        block_names.remove('__datetime__')
    except ValueError:
        pass
    header = list()
    lines = toml_dict.as_string().split('\n')
    for line in lines:
        if line.startswith('#'):
            header.append(line.strip().split('# ')[1])
        if (line == ''):
            break
    date_time = _get_datetime_from_header(header)
    return (date_time, header, block_names, (variables, values, comments, blocks))
