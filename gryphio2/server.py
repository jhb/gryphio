import os
import sys

from chameleon import PageTemplate, PageTemplateLoader
from wtforms import Form, BooleanField, StringField, validators, widgets, SelectField
import flask
from flask import request
from neodb import NeoDB




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
    return TemplateWrapper(templates[name],
                           flask=flask,
                           templates=templates,
                           db=db,
                           request=request)

@api.route('/')
def index():
    query = request.args.get('query')
    if not query:
        query='match (n) return n'
    template = getTemplate('main.pt')
    return template(query=query)

@api.route('/<objtype>/<id>')
def getObject(objtype,id):
    id = int(id)
    if objtype == 'node':
        query = 'match (n) where id(n)={nid} return n limit 1'
        obj = db.run(query,nid=id).single()['n']
        labels = list(obj.labels)
    elif objtype == 'edge':
        query = 'match ()-[r]->() where id(r)={rid} return r limit 1'
        obj = db.run(query,rid=id).single()['r']
        labels = [obj.type]
    template = getTemplate('properties.pt')
    return template(obj=obj,objtype=db.getType(obj),labels=labels)

if __name__ == '__main__':
    print(os.getcwd())
    print('x'*30)
    auth = ("bolt://localhost:7687", "neo4j", "admin")
    db = NeoDB(*auth)
    api.run(debug=1, host='0.0.0.0', port=9000)