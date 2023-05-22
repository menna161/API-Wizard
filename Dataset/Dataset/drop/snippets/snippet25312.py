import lxml.objectify as lxml_objectify
import numpy as np
import pandas as pd


def clean(x):
    return x.drop('Total', axis=1)
