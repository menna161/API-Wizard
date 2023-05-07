import tensorflow as tf
from storybro.generation.gpt2 import model


def sample_sequence(*, hparams, length, start_token=None, batch_size=None, context=None, temperature=1, top_k=0, top_p=1):
    if (start_token is None):
        assert (context is not None), 'Specify exactly one of start_token and context!'
    else:
        assert (context is None), 'Specify exactly one of start_token and context!'
        context = tf.fill([batch_size, 1], start_token)

    def step(hparams, tokens, past=None):
        lm_output = model.model(hparams=hparams, X=tokens, past=past, reuse=tf.AUTO_REUSE)
        logits = lm_output['logits'][(:, :, :hparams.n_vocab)]
        presents = lm_output['present']
        presents.set_shape(model.past_shape(hparams=hparams, batch_size=batch_size))
        return {'logits': logits, 'presents': presents}
    with tf.name_scope('sample_sequence'):

        def body(past, prev, output):
            next_outputs = step(hparams, prev, past=past)
            logits = (next_outputs['logits'][(:, (- 1), :)] / tf.to_float(temperature))
            logits = penalize_used(logits, output)
            logits = top_k_logits(logits, k=top_k)
            logits = top_p_logits(logits, p=top_p)
            samples = tf.multinomial(logits, num_samples=1, output_dtype=tf.int32)
            return [(next_outputs['presents'] if (past is None) else tf.concat([past, next_outputs['presents']], axis=(- 2))), samples, tf.concat([output, samples], axis=1)]
        (past, prev, output) = body(None, context, context)

        def cond(*args):
            return True
        (_, _, tokens) = tf.while_loop(cond=cond, body=body, maximum_iterations=(length - 1), loop_vars=[past, prev, output], shape_invariants=[tf.TensorShape(model.past_shape(hparams=hparams, batch_size=batch_size)), tf.TensorShape([batch_size, None]), tf.TensorShape([batch_size, None])], back_prop=False)
        return tokens
