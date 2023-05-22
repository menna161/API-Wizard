import math
from multiprocessing import Pool
import numpy as np
from fairseq import bleu, options
from fairseq.data import dictionary
from . import rerank_generate, rerank_score_bw, rerank_score_lm, rerank_options, rerank_utils


def match_target_hypo(args, target_outfile, hypo_outfile):
    'combine scores from the LM and bitext models, and write the top scoring hypothesis to a file'
    if (len(args.weight1) == 1):
        res = score_target_hypo(args, args.weight1[0], args.weight2[0], args.weight3[0], args.lenpen[0], target_outfile, hypo_outfile, True, args.normalize)
        rerank_scores = [res]
    else:
        print('launching pool')
        with Pool(32) as p:
            rerank_scores = p.starmap(score_target_hypo, [(args, args.weight1[i], args.weight2[i], args.weight3[i], args.lenpen[i], target_outfile, hypo_outfile, False, args.normalize) for i in range(len(args.weight1))])
    if (len(rerank_scores) > 1):
        best_index = np.argmax(rerank_scores)
        best_score = rerank_scores[best_index]
        print('best score', best_score)
        print('best lenpen', args.lenpen[best_index])
        print('best weight1', args.weight1[best_index])
        print('best weight2', args.weight2[best_index])
        print('best weight3', args.weight3[best_index])
        return (args.lenpen[best_index], args.weight1[best_index], args.weight2[best_index], args.weight3[best_index], best_score)
    else:
        return (args.lenpen[0], args.weight1[0], args.weight2[0], args.weight3[0], rerank_scores[0])
