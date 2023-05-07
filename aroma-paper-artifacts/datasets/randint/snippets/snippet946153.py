import torch
from fairseq.models import register_model, register_model_architecture
from fairseq.models.nat import NATransformerModel


def _sequential_poisoning(s, V, beta=0.33, bos=2, eos=3, pad=1):
    rand_words = torch.randint(low=4, high=V, size=s.size(), device=s.device)
    choices = torch.rand(size=s.size(), device=s.device)
    choices.masked_fill_((((s == pad) | (s == bos)) | (s == eos)), 1)
    replace = (choices < (beta / 3))
    repeat = ((choices >= (beta / 3)) & (choices < ((beta * 2) / 3)))
    swap = ((choices >= ((beta * 2) / 3)) & (choices < beta))
    safe = (choices >= beta)
    for i in range((s.size(1) - 1)):
        rand_word = rand_words[(:, i)]
        next_word = s[(:, (i + 1))]
        self_word = s[(:, i)]
        replace_i = replace[(:, i)]
        swap_i = (swap[(:, i)] & (next_word != 3))
        repeat_i = (repeat[(:, i)] & (next_word != 3))
        safe_i = (safe[(:, i)] | ((next_word == 3) & (~ replace_i)))
        s[(:, i)] = (((self_word * (safe_i | repeat_i).long()) + (next_word * swap_i.long())) + (rand_word * replace_i.long()))
        s[(:, (i + 1))] = ((next_word * (safe_i | replace_i).long()) + (self_word * (swap_i | repeat_i).long()))
    return s
