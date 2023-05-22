from __future__ import annotations
import datetime
import json
import math
import pathlib
from collections import namedtuple
from pathlib import Path
from typing import Any, Dict, List, Optional, Tuple, Union
from .parsers import parse_dict_flat, parse_dict_nested, parse_json_file, parse_phantom_file, parse_toml_file
import tomlkit


def __init__(self, filename: Union[(str, Path)]=None, filetype: str=None, dictionary: Dict=None, dictionary_type: str=None) -> None:
    self.name: str
    self.filepath: Path
    self.config: Dict[(str, ConfigVariable)]
    self.datetime: Optional[datetime.datetime] = None
    self.header: Optional[List[str]] = None
    if (filename is not None):
        if (filetype is None):
            filetype = 'phantom'
        elif isinstance(filetype, str):
            if (filetype.lower() == 'phantom'):
                filetype = 'phantom'
            elif (filetype.lower() == 'json'):
                filetype = 'json'
            elif (filetype.lower() == 'toml'):
                filetype = 'toml'
            else:
                raise ValueError('Cannot determine file type.')
        else:
            raise TypeError('filetype must be str.')
        if isinstance(filename, str):
            filepath = pathlib.Path(filename).expanduser().resolve()
            filename = filepath.name
        elif isinstance(filename, pathlib.Path):
            filepath = filename.expanduser().resolve()
            filename = filepath.name
        if (not filepath.exists()):
            raise FileNotFoundError(f'Cannot find config file: {filename}')
        self.name = filename
        self.filepath = filepath
    else:
        self.name = 'dict'
        if (dictionary is None):
            raise ValueError('Need a file name or dictionary.')
        if (dictionary_type is None):
            dictionary_type = 'flat'
        if (dictionary_type not in ('nested', 'flat')):
            raise ValueError('Cannot determine dictionary type')
    if (filetype is None):
        assert isinstance(dictionary, Dict)
        if (dictionary_type == 'nested'):
            try:
                (date_time, header, block_names, conf) = parse_dict_nested(dictionary)
            except KeyError:
                raise ValueError('Cannot read dictionary; is the dictionary flat?')
        elif (dictionary_type == 'flat'):
            try:
                (date_time, header, block_names, conf) = parse_dict_flat(dictionary)
            except KeyError:
                raise ValueError('Cannot read dictionary; is the dictionary nested?')
        self._initialize(date_time, header, block_names, conf)
    elif (filetype == 'phantom'):
        (date_time, header, block_names, conf) = parse_phantom_file(filepath)
        self._initialize(date_time, header, block_names, conf)
    elif (filetype == 'json'):
        (date_time, header, block_names, conf) = parse_json_file(filepath)
        self._initialize(date_time, header, block_names, conf)
    elif (filetype == 'toml'):
        (date_time, header, block_names, conf) = parse_toml_file(filepath)
        self._initialize(date_time, header, block_names, conf)
