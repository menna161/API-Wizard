import ast
import collections
import inspect
import gast
import numbers
import sys
import types
import typing
from chainer_compiler.elichika.parser.utils import clip_head
from chainer_compiler.elichika.typing.annotation import *
from chainer_compiler.elichika.typing.types import *
from chainer_compiler.elichika.typing.shape_elem import *
from chainer_compiler.elichika.typing import utils
from chainer_compiler.elichika.typing.ext.numpy_functions import *
from chainer_compiler.elichika.typing.ext.chainer_functions import *
from chainer_compiler.elichika.typing.ext.pytorch_functions import *
from chainer_compiler.elichika.typing.std.builtin_functions import *
from chainer_compiler.elichika.typing.std.builtin_ops import *
from chainer_compiler.elichika.typing.std.list_functions import *
import chainer
import chainer.links as L
import numpy as np
import logging
import torch
import torch.nn as nn
from copy import deepcopy
import ast
import gast
import importlib
import sys
import traceback
from astmonkey import transformers, visitors


def infer_function_instance(self, node, func, ty_args, ty_kwargs):
    if (func in numpy_func_ty.keys()):
        return call_function(numpy_func_ty, func, node, ty_args, ty_kwargs)
    if (func in chainer_func_ty.keys()):
        return call_function(chainer_func_ty, func, node, ty_args, ty_kwargs)
    if (func in pytorch_func_ty.keys()):
        return call_function(pytorch_func_ty, func, node, ty_args, ty_kwargs)
    if (type(func) in L.__dict__.values()):
        return call_callable(chainer_callable_ty, func, node, ty_args, ty_kwargs)
    if (type(func) in nn.__dict__.values()):
        if isinstance(func, nn.Sequential):
            (x_type,) = ty_args
            for (idx, module) in enumerate(func.children()):
                x_type = self.infer_function_instance(node, module, [x_type], {})
            return x_type
        return call_callable(pytorch_callable_ty, func, node, ty_args, ty_kwargs)
    if (func in list_func_ty.keys()):
        return call_function(list_func_ty, func, node, ty_args, ty_kwargs)
    if (func in __builtins__.values()):
        if (func in builtin_func_ty.keys()):
            return call_function(builtin_func_ty, func, node, ty_args, {})
        return call_builtin_function(func, node, ty_args)
    return self.infer_user_defined_function(func, ty_args, node)
