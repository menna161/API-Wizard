from argparse import ArgumentParser, Namespace
from enum import Enum
from agent.config import action_generator_args
from agent.config import args
from agent.config import text_encoder_args
from agent.config import state_encoder_args
from agent.config import state_representation_args


def __eq__(self, other) -> bool:
    still_same: bool = (self._task == other.get_task())
    still_same = (still_same and (self._text_encoder_args == other.get_text_encoder_args()))
    still_same = (still_same and (self._state_encoder_args == other.get_state_encoder_args()))
    still_same = (still_same and (self._decoder_args == other.get_decoder_args()))
    return still_same
