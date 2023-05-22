import numpy as np
import warnings


def nsga_sort(objVals, returnFronts=False):
    'Returns ranking of objective values based on non-dominated sorting.\n  Optionally returns fronts (useful for visualization).\n  \n  NOTE: Assumes maximization of objective function\n   \n  Args: \n    objVals - (np_array) - Objective values of each individual\n              [nInds X nObjectives]\n    \n  Returns: \n    rank    - (np_array) - Rank in population of each individual\n            int([nIndividuals X 1])\n    front   - (np_array) - Pareto front of each individual\n            int([nIndividuals X 1]) \n  \n  Todo: \n    * Extend to N objectives\n  '
    fronts = getFronts(objVals)
    for f in range(len(fronts)):
        x1 = objVals[(fronts[f], 0)]
        x2 = objVals[(fronts[f], 1)]
        crowdDist = (getCrowdingDist(x1) + getCrowdingDist(x2))
        frontRank = np.argsort((- crowdDist))
        fronts[f] = [fronts[f][i] for i in frontRank]
    tmp = [ind for front in fronts for ind in front]
    rank = np.empty_like(tmp)
    rank[tmp] = np.arange(len(tmp))
    if (returnFronts is True):
        return (rank, fronts)
    else:
        return rank
