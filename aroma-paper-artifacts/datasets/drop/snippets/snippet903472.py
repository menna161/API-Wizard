import torch
import torch.nn as nn
import torch.nn.functional as F
import math
import copy
from transformers.modeling_gpt2 import *


def forward(self, input_ids, past=None, attention_mask=None, token_type_ids=None, position_ids=None, head_mask=None, labels=None, includeprev=False, x_prev=None):
    if includeprev:
        input_shape = input_ids.size()
        input_ids = input_ids.view((- 1), input_shape[(- 1)])
        if (token_type_ids is not None):
            token_type_ids = token_type_ids.view((- 1), input_shape[(- 1)])
        if (position_ids is not None):
            position_ids = position_ids.view((- 1), input_shape[(- 1)])
        if (past is None):
            past_length = 0
            past = ([None] * len(self.h))
        else:
            past_length = past[0][0].size((- 2))
        if (position_ids is None):
            position_ids = torch.arange(past_length, (input_ids.size((- 1)) + past_length), dtype=torch.long, device=input_ids.device)
            position_ids = position_ids.unsqueeze(0).expand_as(input_ids)
        if (attention_mask is not None):
            attention_mask = attention_mask.view((- 1), input_shape[(- 1)])
            attention_mask = attention_mask.unsqueeze(1).unsqueeze(2)
            attention_mask = attention_mask.to(dtype=next(self.parameters()).dtype)
            attention_mask = ((1.0 - attention_mask) * (- 10000.0))
        if (head_mask is not None):
            if (head_mask.dim() == 1):
                head_mask = head_mask.unsqueeze(0).unsqueeze(0).unsqueeze((- 1)).unsqueeze((- 1))
                head_mask = head_mask.expand(self.config.n_layer, (- 1), (- 1), (- 1), (- 1))
            elif (head_mask.dim() == 2):
                head_mask = head_mask.unsqueeze(1).unsqueeze((- 1)).unsqueeze((- 1))
            head_mask = head_mask.to(dtype=next(self.parameters()).dtype)
        else:
            head_mask = ([None] * self.config.n_layer)
        inputs_embeds = self.wte(input_ids)
        position_embeds = self.wpe(position_ids)
        if (token_type_ids is not None):
            token_type_embeds = self.wte(token_type_ids)
        else:
            token_type_embeds = 0
        x_prev = x_prev.unsqueeze(1)
        inputs_embeds = torch.cat([x_prev, inputs_embeds[(:, 1:, :)]], dim=1)
        hidden_states = ((inputs_embeds + position_embeds) + token_type_embeds)
        hidden_states = self.drop(hidden_states)
        output_shape = (input_shape + (hidden_states.size((- 1)),))
        presents = ()
        all_attentions = []
        all_hidden_states = ()
        for (i, (block, layer_past)) in enumerate(zip(self.h, past)):
            if self.output_hidden_states:
                all_hidden_states = (all_hidden_states + (hidden_states.view(*output_shape),))
            outputs = block(hidden_states, layer_past=layer_past, attention_mask=attention_mask, head_mask=head_mask[i])
            (hidden_states, present) = outputs[:2]
            if self.output_past:
                presents = (presents + (present,))
            if self.output_attentions:
                all_attentions.append(outputs[2])
        hidden_states = self.ln_f(hidden_states)
        hidden_states = hidden_states.view(*output_shape)
        if self.output_hidden_states:
            all_hidden_states = (all_hidden_states + (hidden_states,))
        outputs = (hidden_states,)
        if self.output_past:
            outputs = (outputs + (presents,))
        if self.output_hidden_states:
            outputs = (outputs + (all_hidden_states,))
        if self.output_attentions:
            attention_output_shape = ((input_shape[:(- 1)] + ((- 1),)) + all_attentions[0].shape[(- 2):])
            all_attentions = tuple((t.view(*attention_output_shape) for t in all_attentions))
            outputs = (outputs + (all_attentions,))
        return outputs
    else:
        return super().forward(input_ids, past=past, attention_mask=attention_mask, token_type_ids=token_type_ids, position_ids=position_ids, head_mask=head_mask)
