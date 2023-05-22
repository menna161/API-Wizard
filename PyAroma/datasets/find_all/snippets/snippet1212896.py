from flask import Flask, render_template, redirect, url_for, request, make_response
from pymongo import MongoClient
from bson.objectid import ObjectId
import socket
import os
import json


@staticmethod
def find_all():
    return [RSVP(**doc) for doc in db.rsvpdata.find()]
