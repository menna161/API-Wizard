import pathlib
import phantomconfig as pc
from .stub import test_data


def test_read_toml_config():
    'Test reading TOML config files.'
    conf = pc.read_toml(test_toml_file)
    assert (conf.variables == test_data.variables)
    assert (conf.values == test_data.values)
    assert (conf.header == test_data.header)
    assert (conf.datetime == test_data._datetime)
