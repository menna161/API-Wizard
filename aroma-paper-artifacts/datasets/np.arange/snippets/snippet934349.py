import torch
import gym
import torch.nn as nn
import torch.nn.functional as F
import torch.optim as optim
import numpy as np
from dataclasses import dataclass
from typing import Any
from random import random
from PIL import Image
from agent_and_model import DQNAgent, sars, Model, ReplayBuffer
import plotly.express as px


def plot_score(all_scores):
    fig = px.line(x=np.arange(len(all_scores)), y=all_scores)
    fig.write_html('Play_DQN_CNN_Trend_figure.html')
