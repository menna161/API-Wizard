import torch
import warnings
from collections import namedtuple
from packaging import version
from ...backend.torch_backend import TorchBackend


def _fft(input, inverse=False):
    'Interface with torch FFT routines for 3D signals.\n            fft of a 3d signal\n            Example\n            -------\n            x = torch.randn(128, 32, 32, 32, 2)\n\n            x_fft = fft(x)\n            x_ifft = fft(x, inverse=True)\n            Parameters\n            ----------\n            x : tensor\n                Complex input for the FFT.\n            inverse : bool\n                True for computing the inverse FFT.\n\n            Raises\n            ------\n            TypeError\n                In the event that x does not have a final dimension 2 i.e. not\n                complex.\n\n            Returns\n            -------\n            output : tensor\n                Result of FFT or IFFT.\n        '
    if inverse:
        return torch.view_as_real(torch.fft.ifftn(torch.view_as_complex(input), dim=[(- 1), (- 2), (- 3)]))
    return torch.view_as_real(torch.fft.fftn(torch.view_as_complex(input), dim=[(- 1), (- 2), (- 3)]))
