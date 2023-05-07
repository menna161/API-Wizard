import os
import sys
import config
import psycopg2
import pandas as pd
from datetime import datetime
from urllib.parse import quote_plus
from flask_wtf import Form
from wtforms.fields import SelectField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, ValidationError
from flask import request
from flask_bootstrap import Bootstrap
from flask import render_template, Flask, Response
from flask_paginate import Pagination, get_page_parameter, get_page_args


def chunk_results(offset=0, per_page=10, query_results=[]):
    '\n\tPartition query_results for pagination\n\n\tParameters:\n\toffset (int): offset of the pagination\n\tper_page (int): number of results that will be shown in each page\n\tquery_results (table): data table that will be divided into chunks\n\n\tReturns:\n\tpandas table: chunk of the pandas table that will be displayed on the current page\n\n\t'
    return query_results.iloc[(offset:(offset + per_page), :)]
