from collections import UserList
import uuid
import random
import string

import neo4jdb

counter = {}


def newuid():
    return ''.join(random.choices(string.digits + string.ascii_letters, k=5))
    # counter['uid']=counter.get('uid',0)+1
    # return counter['uid']


RELSPECIALS = ['_source', '_reltype', '_target']

class Node(object):

    def __init__(self, *args, **kwargs):

        if '_uid' not in kwargs:
            kwargs['_uid'] = newuid()
        self._labels = set(args)
        #self._labels.add('Node')
        self.__dict__.update(kwargs)
        self._id=None

    def __str__(self):
        argstring = ', '.join([repr(i) for i in self._labels])
        kwargsstring = ', '.join(
                ['%s=%s' % (k, repr(v)) for k, v in self.__dict__.items() if not k.startswith('_labels')])
        parameterstring = ', '.join([e for e in [argstring, kwargsstring] if e])

        return "%s(%s)" % (self.__class__.__name__, parameterstring)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self._uid)


class Relation(object):

    def __init__(self, _source, _reltype, _target, **kwargs):
        if '_uid' not in kwargs:
            kwargs['_uid'] = newuid()
        self._source = _source
        self._reltype = _reltype
        self._target = _target
        self.__dict__.update(kwargs)

    def __str__(self):
        argstring = ", ".join([repr(self._source), repr(self._reltype), repr(self._target)])
        kwargsstring = ', '.join(
                ['%s=%s' % (k, repr(v)) for k, v in self.__dict__.items() if k not in RELSPECIALS])
        parameterstring = ', '.join([e for e in [argstring, kwargsstring] if e])
        return "%s(%s)" % (self.__class__.__name__, parameterstring)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self._uid)

    def _getProps(self):
        props = {}
        for k, v in self.__dict__.items():
            if k in RELSPECIALS:
                continue
            if type(v) == set:
                v = list(v)
            props[k] = v
        return props

class Path:

    def __init__(self):
        self.nodes = []
        self.relations = []
        self.elements = []


    def __str__(self):
        return 'Path(%s)' % self.elements

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, id(self))

class Graph:

    def __init__(self, db):
        self.db = db
        self.getNode=db.getNode
        self.jump = db.jump
        self.loadSchemas()

    def __getattr__(self,key):
        "proxy to the (neo4j"
        return getattr(self.db,key)

    def getSchema(self,node=None,**kwargs):
        if node is None:
            if kwargs:
                nodes = self.findNodes(**kwargs)
                node = nodes[0]
            else:
                raise Exception('We need something to work with')
        elif not isinstance(node,Node):
            node = self.findNodes(_schemaname=node)[0]

        reltype = '_PROP'

        s = Schema(node)
        r = self.jump(node,'out',reltype)
        for row in r:
            s._props[row.m._techname]=(row.r,row.m)
        return s

    def loadSchemas(self):
        newschemas = {}
        for node in self.findNodes(_schemaname=neo4jdb.exists):
            schema = self.getSchema(node)
            newschemas[schema._schemaname] = schema
        self.schemas = newschemas

    def allNodes(self):
        return [r.n for r in self.db.query('MATCH (n) return n')]

    def exportCypher(self,filters=['Node'],detach=False):

        prefix='meta'
        counter = {}
        counter['export'] = 0


        def swapuid(props):
            if not props['_uid'].startswith(prefix):
                print('swapping',props['_uid'])
                counter['export'] += 1
                props['_uid']='%s%s' % (prefix,counter['export'])
            else:
                counter['export'] = max(counter['export'],int(props['_uid'][len(prefix):]))


        def nodename(node):
            name = attrFromList(node, ['_techname', 'firstname', 'name', '_uid'])
            name = name.lower()
            name = '_' + name
            name = name.replace('__','_')
            return name

        creates = []
        for node in self.findNodes():
            name = nodename(node)
            isnode = 'Node' in node._labels
            labels = [l for l in list(node._labels) if l not in filters]
            #if isnode:
            #    labels.append('Node')

            props = dict(node.__dict__)
            del (props['_labels'])
            print(props['_uid'])
            swapuid(props)
            creates.append('(%s:%s %s)' % (name, ':'.join(labels), self.dict2cypher(props)))

        for row in self.query('MATCH (n)-[r]->(m) return n,r,m'):
            rel = row.r
            source= row.n
            target = row.m
            sourcename = nodename(source)
            targetname = nodename(target)
            props = dict()
            for k,v in rel.__dict__.items():
                if k not in RELSPECIALS:
                    props[k]=v
            swapuid(props)
            creates.append('(%s)-[:`%s` %s]->(%s)' % (sourcename,rel._reltype,self.dict2cypher(props),targetname))
        out= 'CREATE\n'+',\n'.join(creates)+';'
        if detach:
            out = 'MATCH (n) detach delete n;\n\n'+out
        return out

    def checkSchemas(self, node):
        schemanames = set()
        for name,schema in self.schemas.items():
            if schema.checkNode(node):
                schemanames.add(name)
        return schemanames

    def maxArity(self,node,key):
        n = 0
        schemanames = self.checkSchemas(node)
        for name in schemanames:
            schema = self.schemas[name]
            if key in schema._props:
                mi,ma = schema.arity2mm(schema._props[key][0]._arity)
            n = max(n,ma)
        return n


def attrFromList(obj,keys,default=None):
    for key in keys:
        if hasattr(obj,key) and getattr(obj,key):
            return getattr(obj,key)
    return default

class SchemaException(Exception):
    pass

class Schema:

    def __init__(self, node, _props=None):
        self._label = list(node._labels)[0]
        if _props is None:
            _props={}
        self._props = _props
        for k,v in node.__dict__.items():
            setattr(self,k,v)

    def __str__(self):
        return 'Schema(%s)' % self.__dict__

    def getPropKeys(self):
        return tuple(self._props.keys())

    def assignTo(self,node):
        for k,v in self._props.items():
            rel,propnode = v
            amin,amax = self.arity2mm(rel._arity)
            scalartype = propnode._scalartype
            if scalartype == 'string': scalartype='str'
            if amax>1:
                newvalue = []
            else:
                newvalue =  __builtins__.get(scalartype)()
            if not hasattr(node,k):
                setattr(node,k,newvalue)
        return node



    def checkNode(self,node,returnErrors=False):
        errors = {}
        for k,v in self._props.items():
            rel,prop = v
            min,max = self.arity2mm(rel._arity)

            if not hasattr(node,k):
                errors[k]=SchemaException('Must have at least %s %s' % (min,k))
            if min>1:
                if not self.islisty(getattr(node,k)):
                    errors[k]=SchemaException('Must allow for multiple %s' % k)

        if returnErrors:
            return errors
        else:
            return not errors


    def islisty(self,obj):
        return isinstance(obj,(list,tuple))

    def arity2mm(self,arity):
        min=0
        max=0

        try:
            arity = int(arity)
        except:
            pass


        if type(arity)==int:
            min=arity
            max=arity
        elif ',' in arity:
            parts = arity.split(',')
            min = parts[0].strip()
            max = parts[1].strip()
        elif arity=='*':
            max=None
        elif arity=='?':
            max=1
        elif arity=='+':
            min=1
            max=None
        return min,max



