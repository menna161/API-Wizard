import pathlib
import phantomconfig as pc
from .stub import test_data


def test_read_json_config():
    'Test reading JSON config files.'
    conf = pc.read_json(test_json_file)
    assert (conf.config == test_data.config)
    assert (conf.header == test_data.header)
    assert (conf.datetime == test_data._datetime)
