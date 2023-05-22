import os
import matplotlib
import matplotlib.font_manager as font_manager
from jamo import h2j, j2hcj
import matplotlib.pyplot as plt
from text import PAD, EOS
from utils import add_postfix
from text.korean import normalize


def plot(alignment, info, text, isKorean=True):
    (char_len, audio_len) = alignment.shape
    (fig, ax) = plt.subplots(figsize=((char_len / 5), 5))
    im = ax.imshow(alignment.T, aspect='auto', origin='lower', interpolation='none')
    xlabel = 'Encoder timestep'
    ylabel = 'Decoder timestep'
    if (info is not None):
        xlabel += '\n{}'.format(info)
    plt.xlabel(xlabel)
    plt.ylabel(ylabel)
    if text:
        if isKorean:
            jamo_text = j2hcj(h2j(normalize(text)))
        else:
            jamo_text = text
        pad = ([PAD] * ((char_len - len(jamo_text)) - 1))
        A = (([tok for tok in jamo_text] + [EOS]) + pad)
        A = [(x if (x != ' ') else '') for x in A]
        plt.xticks(range(char_len), A)
    if (text is not None):
        while True:
            if (text[(- 1)] in [EOS, PAD]):
                text = text[:(- 1)]
            else:
                break
        plt.title(text)
    plt.tight_layout()
