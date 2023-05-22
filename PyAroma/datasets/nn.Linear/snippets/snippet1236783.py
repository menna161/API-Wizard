from __future__ import annotations
import copy
import logging
from typing import TYPE_CHECKING
import numpy as np
import torch
from torch import nn
from agent import util
from agent.data import partial_observation
from agent.environment import agent_actions
from agent.environment import util as environment_util
from agent.evaluation import distribution_visualizer
from agent.evaluation import plan_metrics
from agent.learning import auxiliary
from agent.learning import batch_util
from agent.learning import sampling
from agent.learning.plan_losses import SpatialSoftmax2d
from agent.model.models import plan_predictor_model
from agent.model.modules import map_distribution_embedder
from agent.model.modules import word_embedder
from agent.model.utilities import initialization
from agent.model.utilities import rnn
from agent.simulation import planner
from agent.simulation import unity_game
from typing import Any, Dict, List, Optional, Tuple
from agent.config import evaluation_args
from agent.config import model_args
from agent.data import instruction_example
from agent.evaluation import evaluation_logger
from agent.environment import state_delta
from agent.simulation import game


def __init__(self, args: model_args.ModelArgs, input_vocabulary: List[str], auxiliaries: List[auxiliary.Auxiliary], load_pretrained: bool=True, end_to_end: bool=False):
    super(ActionGeneratorModel, self).__init__()
    self._args: model_args.ModelArgs = args
    self._end_to_end = end_to_end
    self._plan_predictor: Optional[plan_predictor_model.PlanPredictorModel] = None
    if (self._end_to_end or load_pretrained):
        self._plan_predictor: plan_predictor_model.PlanPredictorModel = plan_predictor_model.PlanPredictorModel(args, input_vocabulary, auxiliaries)
    self._output_layer = None
    self._rnn = None
    self._action_embedder = None
    if self._args.get_decoder_args().use_recurrence():
        self._action_embedder: word_embedder.WordEmbedder = word_embedder.WordEmbedder(self._args.get_decoder_args().get_action_embedding_size(), [str(action) for action in agent_actions.AGENT_ACTIONS], add_unk=False)
        self._rnn: nn.Module = nn.LSTM((self._args.get_decoder_args().get_state_internal_size() + self._args.get_decoder_args().get_action_embedding_size()), self._args.get_decoder_args().get_hidden_size(), self._args.get_decoder_args().get_num_layers(), batch_first=True)
        self._output_layer: nn.Module = nn.Linear((self._args.get_decoder_args().get_hidden_size() + self._args.get_decoder_args().get_state_internal_size()), len(agent_actions.AGENT_ACTIONS))
        torch.nn.init.orthogonal_(self._output_layer.weight, torch.nn.init.calculate_gain('leaky_relu'))
        self._output_layer.bias.data.fill_(0)
    distribution_num_channels: int = 0
    if self._args.get_decoder_args().use_trajectory_distribution():
        distribution_num_channels += 1
    if self._args.get_decoder_args().use_goal_probabilities():
        distribution_num_channels += 1
    if self._args.get_decoder_args().use_obstacle_probabilities():
        distribution_num_channels += 1
    if self._args.get_decoder_args().use_avoid_probabilities():
        distribution_num_channels += 1
    self._map_distribution_embedder: map_distribution_embedder.MapDistributionEmbedder = map_distribution_embedder.MapDistributionEmbedder(distribution_num_channels, self._args.get_decoder_args().get_state_internal_size(), (self._args.get_decoder_args().get_state_internal_size() if self._args.get_decoder_args().use_recurrence() else len(agent_actions.AGENT_ACTIONS)), self._args.get_decoder_args().get_crop_size(), self._args.get_decoder_args().convolution_encode_map_distributions(), self._args.get_decoder_args().use_recurrence())
    if load_pretrained:
        if self._args.get_decoder_args().pretrained_generator():
            initialization.load_pretrained_parameters(self._args.get_decoder_args().pretrained_action_generator_filepath(), module=self)
        if self._args.get_decoder_args().pretrained_plan_predictor():
            initialization.load_pretrained_parameters(self._args.get_decoder_args().pretrained_plan_predictor_filepath(), module=self._plan_predictor)
