import tensorflow as tf
from storybro.generation.gpt2 import model


def body(past, prev, output):
    next_outputs = step(hparams, prev, past=past)
    logits = (next_outputs['logits'][(:, (- 1), :)] / tf.to_float(temperature))
    logits = penalize_used(logits, output)
    logits = top_k_logits(logits, k=top_k)
    logits = top_p_logits(logits, p=top_p)
    samples = tf.multinomial(logits, num_samples=1, output_dtype=tf.int32)
    return [(next_outputs['presents'] if (past is None) else tf.concat([past, next_outputs['presents']], axis=(- 2))), samples, tf.concat([output, samples], axis=1)]
