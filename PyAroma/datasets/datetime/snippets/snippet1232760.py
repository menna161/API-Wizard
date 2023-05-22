import pathlib
import phantomconfig as pc
from .stub import test_data


def test_write_toml_config():
    'Test writing TOML config files.'
    tmp_file = pathlib.Path('tmp.toml')
    conf = pc.read_config(test_phantom_file)
    conf.write_toml(tmp_file)
    conf = pc.read_toml(tmp_file)
    assert (conf.variables == test_data.variables)
    assert (conf.values == test_data.values)
    assert (conf.header == test_data.header)
    assert (conf.datetime == test_data._datetime)
    tmp_file.unlink()
