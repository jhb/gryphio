from collections import UserList
import uuid
import random
import string

counter = {}


def newuid():
    return ''.join(random.choices(string.digits + string.ascii_letters, k=5))
    # counter['uid']=counter.get('uid',0)+1
    # return counter['uid']


RELSPECIALS = ['source', 'reltype', 'target']

class Node(object):

    def __init__(self, *args, **kwargs):

        if '_uid' not in kwargs:
            kwargs['_uid'] = newuid()
        self._labels = set(args)
        self._labels.add('Node')
        self.__dict__.update(kwargs)

    def __str__(self):
        argstring = ', '.join([repr(i) for i in self._labels])
        kwargsstring = ', '.join(
                ['%s=%s' % (k, repr(v)) for k, v in self.__dict__.items() if (k=='_uid') or not k.startswith('_')])
        parameterstring = ', '.join([e for e in [argstring, kwargsstring] if e])

        return "%s(%s)" % (self.__class__.__name__, parameterstring)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self._uid)


class Relation(object):

    def __init__(self, _source, _reltype, _target, _uid=None, **kwargs):
        self._uid=None
        if '_uid' not in kwargs:
            kwargs['_uid'] = newuid()
        self._source = _source
        self._reltype = _reltype
        self._target = _target
        self.__dict__.update(kwargs)

    def __str__(self):
        argstring = ", ".join([str(self._source), repr(self._reltype), str(self._target)])
        kwargsstring = ', '.join(
                ['%s=%s' % (k, repr(v)) for k, v in self.__dict__.items() if k not in RELSPECIALS])
        parameterstring = ', '.join([e for e in [argstring, kwargsstring] if e])
        return "%s(%s)" % (self.__class__.__name__, parameterstring)

    def __repr__(self):
        return '<%s %s>' % (self.__class__.__name__, self._uid)

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
        self.storeNode = db.storeNode
        self.findNodes = db.findNodes

    def getSchema(self,node):
        if not isinstance(node,Node):
            node = self.getNode(node)

        reltype = 'SEM_PROP'

        s = Schema(node)
        r = self.jump(node,'out',reltype)
        for row in r:
            s._props[row.m.techname]=(row.r,row.m)
        return s

    def getNodes(self):
        return [r.n for r in self.db.query('MATCH (n) return n')]


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
            amin,amax = self.arity2mm(rel.arity)
            scalartype = propnode.scalartype
            if scalartype == 'string': scalartype='str'
            if amax>1:
                newvalue = []
            else:
                newvalue =  __builtins__.get(scalartype)()
            if not hasattr(node,k):
                setattr(node,k,newvalue)
        return node



    def checkNode(self,node):
        errors = {}
        for k,v in self._props.items():
            rel,prop = v
            min,max = self.arity2mm(rel.arity)
            if min>0:
                if not hasattr(node,k):
                    errors[k]=SchemaException('Must have at least %s %s' % (min,k))
            if min>1:
                if not self.islisty(getattr(node,k)):
                    errors[k]=SchemaException('Must allow for multiple %s' % k)
        return errors

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



