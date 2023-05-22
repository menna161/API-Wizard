from __future__ import annotations
from typing import TYPE_CHECKING
import torch
import torch.nn as nn
from agent import util
from agent.environment import agent
from agent.environment import position
from agent.environment import state_delta
from agent.environment import util as environment_util
from agent.learning import auxiliary
from agent.learning import batch_util
from agent.model.map_transformations import map_transformer
from agent.model.map_transformations import pose
from agent.model.modules import dynamic_environment_embedder
from agent.model.modules import lingunet
from agent.model.modules import state_representation
from agent.model.modules import static_environment_embedder
from agent.model.modules import text_encoder
from agent.model.modules import word_embedder
from agent.config import model_args
from agent.config import state_representation_args
from agent.data import instruction_example
from agent.data import partial_observation
from typing import Any, List, Dict, Optional, Tuple


def __init__(self, args: model_args.ModelArgs, input_vocabulary: List[str], auxiliaries: List[auxiliary.Auxiliary]):
    super(PlanPredictorModel, self).__init__()
    self._args: model_args.ModelArgs = args
    self._env_feature_channels: int = 0
    self._auxiliaries: List[auxiliary.Auxiliary] = auxiliaries
    state_rep_args: state_representation_args.StateRepresentationArgs = self._args.get_state_rep_args()
    self._state_rep: state_representation.StateRepresentation = state_representation.StateRepresentation(state_rep_args)
    self._static_embedder: static_environment_embedder.StaticEnvironmentEmbedder = static_environment_embedder.StaticEnvironmentEmbedder(self._state_rep, state_rep_args.get_property_embedding_size(), (not state_rep_args.learn_absence_embeddings()))
    self._dynamic_embedder: dynamic_environment_embedder.DynamicEnvironmentEmbedder = dynamic_environment_embedder.DynamicEnvironmentEmbedder(self._state_rep, state_rep_args.get_property_embedding_size(), (not state_rep_args.learn_absence_embeddings()))
    self._env_feature_channels = self._static_embedder.embedding_size()
    self._instruction_encoder: text_encoder.TextEncoder = text_encoder.TextEncoder(self._args.get_text_encoder_args(), input_vocabulary)
    text_feature_size = self._args.get_text_encoder_args().get_hidden_size()
    self._grounding_map_channels = 4
    self._initial_text_kernel_ll = nn.Linear(text_feature_size, (self._env_feature_channels * self._grounding_map_channels))
    self._intermediate_goal_ll: Optional[nn.Module] = None
    if (auxiliary.Auxiliary.INTERMEDIATE_GOALS in auxiliaries):
        self._intermediate_goal_ll = nn.Linear(self._grounding_map_channels, 1, bias=False)
    self._into_lingunet_transformer: map_transformer.MapTransformer = map_transformer.MapTransformer(source_map_size=environment_util.ENVIRONMENT_WIDTH, dest_map_size=environment_util.PADDED_WIDTH, world_size_px=environment_util.ENVIRONMENT_WIDTH, world_size_m=environment_util.ENVIRONMENT_WIDTH)
    self._after_lingunet_transformer: map_transformer.MapTransformer = map_transformer.MapTransformer(source_map_size=environment_util.PADDED_WIDTH, dest_map_size=environment_util.ENVIRONMENT_WIDTH, world_size_px=environment_util.PADDED_WIDTH, world_size_m=environment_util.PADDED_WIDTH)
    if (torch.cuda.device_count() >= 1):
        self._into_lingunet_transformer = self._into_lingunet_transformer.cuda(device=util.DEVICE)
        self._after_lingunet_transformer = self._after_lingunet_transformer.cuda(device=util.DEVICE)
    lingunet_out_channels: int = 0
    extra_head_channels: int = 0
    if (auxiliary.Auxiliary.FINAL_GOALS in auxiliaries):
        lingunet_out_channels += 1
    if (auxiliary.Auxiliary.TRAJECTORY in auxiliaries):
        lingunet_out_channels += 1
    if (auxiliary.Auxiliary.AVOID_LOCS in auxiliaries):
        lingunet_out_channels += 1
    if (auxiliary.Auxiliary.OBSTACLES in auxiliaries):
        lingunet_out_channels += 1
    self._lingunet = lingunet.LingUNet(self._args.get_state_encoder_args(), (self._env_feature_channels + self._grounding_map_channels), text_feature_size, lingunet_out_channels, self._args.get_dropout(), extra_head_channels=extra_head_channels, input_img_size=environment_util.PADDED_WIDTH, layer_single_preds=(auxiliary.Auxiliary.IMPLICIT in self._auxiliaries))
