import sys
import os
import argparse
import json
import logging
from penman.__about__ import __version__
from penman.model import Model
from penman import layout
from penman.codec import PENMANCodec
from penman import transform
from penman.models.amr import model
from penman.models.noop import model


def _get_model(amr, noop, model_file):
    if amr:
        from penman.models.amr import model
    elif noop:
        from penman.models.noop import model
    elif model_file:
        model = Model(**json.load(model_file))
    else:
        model = Model()
    return model
