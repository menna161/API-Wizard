from __future__ import absolute_import, division, print_function
import argparse
from io import open
import torch
from pytorch_pretrained_bert.modeling_gpt2 import CONFIG_NAME, WEIGHTS_NAME, GPT2Config, GPT2Model, load_tf_weights_in_gpt2


def convert_gpt2_checkpoint_to_pytorch(gpt2_checkpoint_path, gpt2_config_file, pytorch_dump_folder_path):
    if (gpt2_config_file == ''):
        config = GPT2Config()
    else:
        config = GPT2Config(gpt2_config_file)
    model = GPT2Model(config)
    load_tf_weights_in_gpt2(model, gpt2_checkpoint_path)
    pytorch_weights_dump_path = ((pytorch_dump_folder_path + '/') + WEIGHTS_NAME)
    pytorch_config_dump_path = ((pytorch_dump_folder_path + '/') + CONFIG_NAME)
    print('Save PyTorch model to {}'.format(pytorch_weights_dump_path))
    torch.save(model.state_dict(), pytorch_weights_dump_path)
    print('Save configuration file to {}'.format(pytorch_config_dump_path))
    with open(pytorch_config_dump_path, 'w', encoding='utf-8') as f:
        f.write(config.to_json_string())
