import datetime
import random
import unittest
import genetic


def mutate(genes, validationRules):
    selectedRule = next((rule for rule in validationRules if (genes[rule.Index] == genes[rule.OtherIndex])))
    if (selectedRule is None):
        return
    if (((index_row(selectedRule.OtherIndex) % 3) == 2) and (random.randint(0, 10) == 0)):
        sectionStart = section_start(selectedRule.Index)
        current = selectedRule.OtherIndex
        while (selectedRule.OtherIndex == current):
            shuffle_in_place(genes, sectionStart, 80)
            selectedRule = next((rule for rule in validationRules if (genes[rule.Index] == genes[rule.OtherIndex])))
        return
    row = index_row(selectedRule.OtherIndex)
    start = (row * 9)
    indexA = selectedRule.OtherIndex
    indexB = random.randrange(start, len(genes))
    (genes[indexA], genes[indexB]) = (genes[indexB], genes[indexA])
