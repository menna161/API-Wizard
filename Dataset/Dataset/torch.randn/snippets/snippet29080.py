import pytest
import torch
import torch.nn as nn
from nbdt.models import ResNet18


@pytest.fixture
def input_cifar10():
    return torch.randn(1, 3, 32, 32)
