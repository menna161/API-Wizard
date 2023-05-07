from flask import Flask, redirect, session, request, render_template, url_for, flash, jsonify, send_file, make_response
from helpers.s3 import S3
from helpers.constants import Constants
from helpers.githubuser import GithubUser, PublicGithubUser
from helpers.githubbot import GithubBot
from helpers.sources.osenv import OSConstants
from helpers.sources.mongo import MongoConstants
from helpers.extensions import LanguageExtensions
import os, time, datetime


@app.route('/go/<path:object_key>')
def go_view(object_key):
    url = url_for('{}_view'.format(constants.get('MODE')), object_key=object_key)
    response = redirect('{}?{}'.format(url, request.query_string))
    return cached(response, datetime.datetime.utcnow(), expires=0)
