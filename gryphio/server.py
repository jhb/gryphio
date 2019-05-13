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

@api.route('/node/<nid>', methods=['POST', 'GET'])
def node(nid=7):

    if 'delete' in request.args:
        delNodeProperty(nid,request.args['delete'])
        flask.flash('%s removed from node' % request.args['delete'])
        return flask.redirect(request.base_url)

    if nid!='new':
        node = getNode(int(nid))
    else:
        node = DictObject([])

    # if request.method=='GET':

    # build the form
    class MyForm(Form):
        pass



    if request.method=='POST':
        items = request.form.items()
    else:
        items = node.items()

    items = list(items)
    itemsd = dict(items)
    sproperties = getSemProperties()
    for k,v in sorted(items):
        if k.startswith('new_'):
            continue
        scalartype = sproperties[k]['scalartype']

        if scalartype == 'string':
            setattr(MyForm,k,StringField(k,description=sproperties[k].get('description','no description')))

    #setattr(MyForm,'newvalue',StringField('newvalue'))
    choices = [('','Select new attribute')]
    print(items)
    for k,v in sproperties.items():
        if k not in itemsd:
            choices.append((k,'%s - %s' % (k,v['description'])))
    MyForm.new_attribute=SelectField('New Attribute', description='A new attribute for this object', choices=choices)
    MyForm.new_value=StringField('New Value',description='The value of the new property')

    form = MyForm(request.form,DictObject(items))
    if request.method=='POST' and form.validate():
        statement = updateNode(nid,items)
        flask.flash('Node %s updated <small> -- %s</small>' % (nid,statement))
        return flask.redirect('/nodelist#%s' % nid)
    template = getTemplate('nodeform.pt')

    schemas = getSchemas()
    return template(form=form,node=node,sproperties=sproperties,schemas=schemas)

if __name__ == '__main__':
    print(os.getcwd())
    print('x'*30)
    db = Neo4jDB(*auth)
    graph = Graph(db)
    api.run(debug=1,port=9000)
