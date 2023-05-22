from __future__ import absolute_import, division
from collections import OrderedDict
from importlib import import_module
import logging
import os
import sys
import tempfile
from astropy.io import ascii as asc
import jinja2
import pandas as pd
import pdfkit
import requests
import roman
from varcode import load_vcf_fast
from .manufacturability import ManufacturabilityScores
from xvfbwrapper import Xvfb


def _query_wustl(self, predicted_effect, gene_name):
    '\n        Returns a link to the WUSTL page for this variant, if present.\n        '
    amino_acids = predicted_effect.short_description
    api_url = ('http://www.docm.info/api/v1/variants.json?amino_acids=%s&genes=%s' % (amino_acids, gene_name.upper()))
    logger.info('WUSTL link: %s', api_url)
    try:
        contents = requests.get(api_url).json()
        if (len(contents) > 0):
            hgvs = contents[0]['hgvs']
            link_for_report = ('http://docm.genome.wustl.edu/variants/%s' % hgvs)
            logger.info('Link for report: %s', link_for_report)
            return link_for_report
    except requests.exceptions.ConnectionError as e:
        logger.warn('ConnectionError reaching WUSTL: %s', e)
        return None
    logger.info('Variant not found in WUSTL')
    return None
