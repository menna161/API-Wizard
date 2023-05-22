from rdflib import Graph, BNode, Literal, URIRef
from rdflib.namespace import FOAF
from flask import Flask
import flask_rdf
import random


@app.route('/')
@app.route('/<path:path>')
@custom_decorator
def random_age(path=''):
    graph = Graph('IOMemory', BNode())
    graph.add((URIRef(path), FOAF.age, Literal(random.randint(20, 50))))
    return graph
