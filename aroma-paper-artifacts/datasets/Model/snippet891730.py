from __future__ import absolute_import, division, print_function
import argparse
from io import open
import torch
from pytorch_pretrained_bert.modeling_openai import CONFIG_NAME, WEIGHTS_NAME, OpenAIGPTConfig, OpenAIGPTModel, load_tf_weights_in_openai_gpt


def convert_openai_checkpoint_to_pytorch(openai_checkpoint_folder_path, openai_config_file, pytorch_dump_folder_path):
    if (openai_config_file == ''):
        config = OpenAIGPTConfig()
    else:
        config = OpenAIGPTConfig(openai_config_file)
    model = OpenAIGPTModel(config)
    load_tf_weights_in_openai_gpt(model, openai_checkpoint_folder_path)
    pytorch_weights_dump_path = ((pytorch_dump_folder_path + '/') + WEIGHTS_NAME)
    pytorch_config_dump_path = ((pytorch_dump_folder_path + '/') + CONFIG_NAME)
    print('Save PyTorch model to {}'.format(pytorch_weights_dump_path))
    torch.save(model.state_dict(), pytorch_weights_dump_path)
    print('Save configuration file to {}'.format(pytorch_config_dump_path))
    with open(pytorch_config_dump_path, 'w', encoding='utf-8') as f:
        f.write(config.to_json_string())
