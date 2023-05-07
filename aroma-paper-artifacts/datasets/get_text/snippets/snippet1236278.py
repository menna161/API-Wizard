from argparse import ArgumentParser, Namespace
from enum import Enum
from agent.config import action_generator_args
from agent.config import args
from agent.config import text_encoder_args
from agent.config import state_encoder_args
from agent.config import state_representation_args


def get_text_encoder_args(self) -> text_encoder_args.TextEncoderArgs:
    self.check_initialized()
    return self._text_encoder_args
