import datetime
import random
import sys
import unittest
import genetic


def mutate(genes, items, maxWeight, maxVolume, window):
    window.slide()
    fitness = get_fitness(genes)
    remainingWeight = (maxWeight - fitness.TotalWeight)
    remainingVolume = (maxVolume - fitness.TotalVolume)
    removing = ((len(genes) > 1) and (random.randint(0, 10) == 0))
    if removing:
        index = random.randrange(0, len(genes))
        iq = genes[index]
        item = iq.Item
        remainingWeight += (item.Weight * iq.Quantity)
        remainingVolume += (item.Volume * iq.Quantity)
        del genes[index]
    adding = (((remainingWeight > 0) or (remainingVolume > 0)) and ((len(genes) == 0) or ((len(genes) < len(items)) and (random.randint(0, 100) == 0))))
    if adding:
        newGene = add(genes, items, remainingWeight, remainingVolume)
        if (newGene is not None):
            genes.append(newGene)
            return
    index = random.randrange(0, len(genes))
    iq = genes[index]
    item = iq.Item
    remainingWeight += (item.Weight * iq.Quantity)
    remainingVolume += (item.Volume * iq.Quantity)
    changeItem = ((len(genes) < len(items)) and (random.randint(0, 4) == 0))
    if changeItem:
        itemIndex = items.index(iq.Item)
        start = max(1, (itemIndex - window.Size))
        stop = min((len(items) - 1), (itemIndex + window.Size))
        item = items[random.randint(start, stop)]
    maxQuantity = max_quantity(item, remainingWeight, remainingVolume)
    if (maxQuantity > 0):
        genes[index] = ItemQuantity(item, (maxQuantity if (window.Size > 1) else random.randint(1, maxQuantity)))
    else:
        del genes[index]
