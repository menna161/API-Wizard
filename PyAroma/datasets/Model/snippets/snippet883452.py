import math
import os
from collections import OrderedDict
from dataclasses import field, dataclass
from torch import nn
from typing import Dict, List, Union, Callable
from models import Seq2Seq
from sonosco.models.modules import MaskConv, BatchRNN, SequenceWise, InferenceBatchSoftmax
from sonosco.model.serializer import Serializer
from sonosco.model.deserializer import Deserializer
from sonosco.model.serialization import serializable
from abc import ABC, abstractmethod


def test_model_serialization():
    rnn_type: type = nn.GRU
    labels: str = 'ABCD'
    rnn_hid_size: int = 256
    nb_layers: int = 10
    audio_conf: Dict[(str, str)] = {'key': 'value'}
    bidirectional: bool = False
    version: str = '1.0.0'
    model_path = 'model'
    saver = Serializer()
    loader = Deserializer()
    model = MockModel(rnn_type=rnn_type, labels=labels, rnn_hid_size=rnn_hid_size, nb_layers=nb_layers, audio_conf=audio_conf, bidirectional=bidirectional, version=version, mockedNestedClass=MockedNestedClass(some_int=42, some_collection=['the', 'future', 'is', 'here'], yetAnotherSerializableClass=YetAnotherSerializableClass(some_stuff='old man')))
    saver.serialize(model, model_path)
    deserialized_model = loader.deserialize(MockModel, model_path, external_args={'labels': 'XD12', 'version': '1.0.1'})
    os.remove(model_path)
    assert (len(deserialized_model.state_dict()) == len(model.state_dict()))
    assert (deserialized_model.state_dict()['conv.seq_module.0.weight'][0][0][0][0] == model.state_dict()['conv.seq_module.0.weight'][0][0][0][0])
    assert (deserialized_model.state_dict()['conv.seq_module.0.weight'][0][0][0][1] == model.state_dict()['conv.seq_module.0.weight'][0][0][0][1])
    assert (deserialized_model.state_dict()['conv.seq_module.0.weight'][0][0][0][5] == model.state_dict()['conv.seq_module.0.weight'][0][0][0][5])
    assert (deserialized_model.rnn_type == rnn_type)
    assert (deserialized_model.labels == 'XD12')
    assert (deserialized_model.rnn_hid_size == rnn_hid_size)
    assert (deserialized_model.nb_layers == nb_layers)
    assert (deserialized_model.audio_conf == audio_conf)
    assert (deserialized_model.bidirectional == bidirectional)
    assert (deserialized_model.version == '1.0.1')
    assert (deserialized_model.mockedNestedClass.some_int == 42)
    assert (deserialized_model.mockedNestedClass.some_collection == ['the', 'future', 'is', 'here'])
    assert (deserialized_model.mockedNestedClass.yetAnotherSerializableClass.some_stuff == 'old man')
