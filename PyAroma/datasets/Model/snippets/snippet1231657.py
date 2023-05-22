from __future__ import absolute_import
from cobra.core.object import Object
from cobra.core import Model
from cobra.core import DictList
from cobra.core import Reaction
from medusa.core.member import Member
from medusa.core.feature import Feature
from pickle import dump
import cobra
import random
import pandas as pd


def __init__(self, list_of_models=[], identifier=None, name=None):
    Object.__init__(self, identifier, name)
    if (len(list_of_models) > 1):
        if (not all((isinstance(x, Model) for x in list_of_models))):
            raise AttributeError('list_of_models may only contain cobra.core.Model objects')
        if (len([model.id for model in list_of_models]) > len(set([model.id for model in list_of_models]))):
            raise AssertionError('Ensemble members cannot have duplicate model ids.')
        self.features = DictList()
        self._populate_features_base(list_of_models)
        self.members = DictList()
        self._populate_members(list_of_models)
    elif (len(list_of_models) == 0):
        self.base_model = Model(id_or_model=(identifier + '_base_model'), name=name)
    else:
        if (not isinstance(list_of_models[0], Model)):
            raise AttributeError('list_of_models may only contain cobra.core.Model objects')
        self.base_model = list_of_models[0]
