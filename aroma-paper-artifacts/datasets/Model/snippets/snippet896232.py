import inspect
import torch.nn as nn
from fairseq.legacy_distributed_data_parallel import LegacyDistributedDataParallel
from fairseq.models import BaseFairseqModel


def DistributedFairseqModel(args, model):
    '\n    Wrap a *model* to support distributed data parallel training.\n\n    This is similar to the built-in DistributedDataParallel, but allows\n    additional configuration of the DistributedDataParallel class to\n    use, and also provides easier access to the wrapped model by\n    forwarding requests for missing attributes to the wrapped model.\n\n    Args:\n        args (argparse.Namespace): fairseq args\n        model (BaseFairseqModel): model to wrap\n    '
    assert isinstance(model, nn.Module)
    if (args.ddp_backend == 'c10d'):
        ddp_class = nn.parallel.DistributedDataParallel
        init_kwargs = dict(module=model, device_ids=[args.device_id], output_device=args.device_id, broadcast_buffers=False, bucket_cap_mb=args.bucket_cap_mb)
        if ('check_reduction' in inspect.getargspec(ddp_class)[0]):
            init_kwargs['check_reduction'] = True
        if ('find_unused_parameters' in inspect.getargspec(ddp_class)[0]):
            init_kwargs['find_unused_parameters'] = args.find_unused_parameters
    elif (args.ddp_backend == 'no_c10d'):
        ddp_class = LegacyDistributedDataParallel
        init_kwargs = dict(module=model, world_size=args.distributed_world_size, buffer_size=(2 ** 28))
    else:
        raise ValueError(('Unknown --ddp-backend: ' + args.ddp_backend))

    class _DistributedFairseqModel(ddp_class):
        'Extend DistributedDataParallel to check for missing\n        attributes in the wrapped module.'

        def __init__(self, *args, **kwargs):
            super().__init__(*args, **kwargs)

        def __getattr__(self, name):
            wrapped_module = super().__getattr__('module')
            if hasattr(wrapped_module, name):
                return getattr(wrapped_module, name)
            return super().__getattr__(name)
    return _DistributedFairseqModel(**init_kwargs)
