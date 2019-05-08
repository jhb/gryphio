import os
import sys

from chameleon import PageTemplate, PageTemplateLoader
from wtforms import Form, BooleanField, StringField, validators, widgets, SelectField
import flask
from flask import request
from graph import *
from config import auth
from neo4jdb import Neo4jDB


api = flask.Flask(__name__)
api.secret_key = b'GryphIsGreat'

class TemplateWrapper:

    def __init__(self,template,**kwargs):
        self.template=template
        self.kwargs=kwargs

    def __call__(self,**kwargs):
        kwargs.update(self.kwargs)
        return self.template(**kwargs)

def getTemplate(name):
    templates = PageTemplateLoader(os.path.join('templates'),'.pt')
    print(templates)
    return TemplateWrapper(templates[name],flask=flask,templates=templates)


@api.route('/test')
def test():
    template = getTemplate('main.pt')
    return template()

@api.route('/nodelist')
def nodelist():
    nodes = graph.getNodes()
    template = getTemplate('nodelist.pt')
    return template(nodes=nodes)

if __name__ == '__main__':
    print(os.getcwd())
    print('x'*30)
    db = Neo4jDB(*auth)
    graph = Graph(db)
    api.run(debug=1,port=9000)
