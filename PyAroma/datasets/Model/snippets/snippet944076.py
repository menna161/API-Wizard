from torch import nn
from fairseq import utils
from fairseq.criterions import FairseqCriterion, register_criterion


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
