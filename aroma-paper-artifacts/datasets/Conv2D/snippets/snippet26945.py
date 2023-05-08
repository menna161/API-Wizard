import typing
import keras
import matchzoo
from matchzoo.engine.base_model import BaseModel
from matchzoo.engine.param import Param
from matchzoo.engine.param_table import ParamTable
from matchzoo.engine import hyper_spaces


@classmethod
def _conv_block(cls, x, kernel_count: int, kernel_size: int, padding: str, activation: str) -> typing.Any:
    output = keras.layers.Conv2D(kernel_count, kernel_size, padding=padding, activation=activation)(x)
    return output
