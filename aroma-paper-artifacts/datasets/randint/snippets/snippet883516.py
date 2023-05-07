import logging
from typing import List, Optional
import torch
import librosa
import numpy as np
import scipy.signal
import sonosco.common.audio_tools as audio_tools
import sonosco.common.utils as utils
import sonosco.common.noise_makers as noise_makers


def augment_audio(self, sound: np.ndarray, stretch: bool=True, shift: bool=False, pitch: bool=True, noise: bool=True) -> np.ndarray:
    '\n        Augments the audio with given parameters/\n        Args:\n            sound:\n            stretch:\n            shift:\n            pitch:\n            noise:\n\n        Returns: augmented audio\n\n        '
    augmented = (audio_tools.stretch(sound, utils.random_float(MIN_STRETCH, MAX_STRETCH)) if stretch else sound)
    augmented = (audio_tools.shift(augmented, np.random.randint(MAX_SHIFT)) if shift else augmented)
    augmented = (audio_tools.pitch_shift(augmented, self.sample_rate, n_steps=utils.random_float(MIN_PITCH, MAX_PITCH)) if pitch else augmented)
    if noise:
        noise_maker = noise_makers.GaussianNoiseMaker()
        augmented = (noise_maker.add_noise(augmented) if noise else augmented)
    return augmented
