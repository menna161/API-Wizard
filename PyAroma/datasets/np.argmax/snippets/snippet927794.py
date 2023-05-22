import numpy as np
from utils import *


def assignOffspring(self, species, pop, p):
    "Assigns number of offspring to each species based on fitness sharing.\n  NOTE: Ordinal rather than the cardinal fitness of canonical NEAT is used.\n\n  Args:\n    species - (Species) - this generation's species\n      .members    - [Ind]   - individuals in species\n    pop     - [Ind]     - individuals with species assigned\n      .fitness    - (float) - performance on task (higher is better)\n    p       - (Dict)    - algorithm hyperparameters\n\n  Returns:\n    species - (Species) - This generation's species\n      .nOffspring - (int) - number of children to produce\n  "
    nSpecies = len(species)
    if (nSpecies == 1):
        species[0].offspring = p['popSize']
    else:
        popFit = np.asarray([ind.fitness for ind in pop])
        popRank = tiedRank(popFit)
        if (p['select_rankWeight'] == 'exp'):
            rankScore = (1 / popRank)
        elif (p['select_rankWeight'] == 'lin'):
            rankScore = (1 + abs((popRank - len(popRank))))
        else:
            print('Invalid rank weighting (using linear)')
            rankScore = (1 + abs((popRank - len(popRank))))
        specId = np.asarray([ind.species for ind in pop])
        speciesFit = np.zeros((nSpecies, 1))
        speciesTop = np.zeros((nSpecies, 1))
        for iSpec in range(nSpecies):
            if (not np.any((specId == iSpec))):
                speciesFit[iSpec] = 0
            else:
                speciesFit[iSpec] = np.mean(rankScore[(specId == iSpec)])
                speciesTop[iSpec] = np.max(popFit[(specId == iSpec)])
                if (speciesTop[iSpec] > species[iSpec].bestFit):
                    species[iSpec].bestFit = speciesTop[iSpec]
                    bestId = np.argmax(popFit[(specId == iSpec)])
                    species[iSpec].bestInd = species[iSpec].members[bestId]
                    species[iSpec].lastImp = 0
                else:
                    species[iSpec].lastImp += 1
                if (species[iSpec].lastImp > p['spec_dropOffAge']):
                    speciesFit[iSpec] = 0
        if (sum(speciesFit) == 0):
            speciesFit = np.ones((nSpecies, 1))
            print('WARN: Entire population stagnant, continuing without extinction')
        offspring = bestIntSplit(speciesFit, p['popSize'])
        for iSpec in range(nSpecies):
            species[iSpec].nOffspring = offspring[iSpec]
    species[:] = [s for s in species if (s.nOffspring != 0)]
    return species
