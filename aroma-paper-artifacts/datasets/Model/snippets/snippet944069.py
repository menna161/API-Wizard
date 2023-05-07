from torch import nn
from fairseq import utils
from fairseq.criterions import FairseqCriterion, register_criterion


@classmethod
def build_criterion(cls, args, task):
    underlying_criterion = CompositeLoss.build_underlying_criterion(args, task)

    class FakeModel(nn.Module):

        def __init__(self, model, net_out, target):
            super().__init__()
            self.model = model
            self.net_out = net_out
            self.target = target

        def forward(self, **unused):
            return self.net_out

        def get_normalized_probs(self, net_output, log_probs, sample=None):
            return self.model.get_normalized_probs(net_output, log_probs, sample=sample)

        def get_targets(self, *unused):
            return self.target

        @property
        def decoder(self):
            return self.model.decoder

    class _CompositeLoss(FairseqCriterion):

        def __init__(self, task, underlying_criterion):
            super().__init__(task)
            self.underlying_criterion = underlying_criterion

        def forward(self, model, sample, reduce=True):
            net_outputs = model(**sample['net_input'])
            targets = sample['target']
            bsz = targets[0].size(0)
            loss = net_outputs[0][0].new((1 if reduce else bsz)).float().zero_()
            sample_size = 0
            logging_output = {}
            for (o, t) in zip(net_outputs[0], targets):
                m = FakeModel(model, (o, net_outputs[1]), t)
                sample['target'] = t
                (l, ss, logging_output) = self.underlying_criterion(m, sample, reduce)
                loss += l
                sample_size += ss
            loss.div_(len(targets))
            sample_size /= len(targets)
            logging_output['loss'] = (utils.item(loss.data) if reduce else loss.data)
            return (loss, sample_size, logging_output)

        @staticmethod
        def aggregate_logging_outputs(logging_outputs):
            return underlying_criterion.__class__.aggregate_logging_outputs(logging_outputs)

        @staticmethod
        def reduce_metrics(logging_outputs) -> None:
            underlying_criterion.__class__.reduce_metrics(logging_outputs)
    return _CompositeLoss(task, underlying_criterion)
