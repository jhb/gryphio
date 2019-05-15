import neo4j
from graph import  Node, Relation, Path, RELSPECIALS, PREFIX

class Neo4jDB():

    def __init__(self,uri,login,passwd):
        self.driver = neo4j.GraphDatabase.driver(uri, auth=(login, passwd))
        self.session = self.driver.session()
        self.tx = None
        self._neonodecache = {}
        self._idnodecache = {}
        self._uidnodecache = {}
        self._relationcache = {}
        self._uidrelationcache = {}

    def begin(self):
        self.tx = self.session.begin_transaction()
        self._neonodecache = {}
        self._relationcache = {}

    def commit(self):
        self.tx.commit()
        self.tx = None

    def rollback(self):
        self.tx.rollback()
        self.tx = None

    def _nodeN2G(self, neonode):
        if neonode not in self._neonodecache:
            node = Node(*neonode.labels, **dict(neonode.items()))
            self._neonodecache[neonode]=node
            node._labels = set(node._labels)
            node._id=neonode.id
        node = self._neonodecache[neonode]
        self._idnodecache[node._id] = node
        self._uidnodecache[node._uid] = node
        return node

    def _relN2G(self,neorel):
        if neorel not in self._relationcache:
            relation = Relation(self.getNodeById(neorel.start_node.id), #self._nodeN2G(neorel.start_node),
                            neorel.type,
                            self.getNodeById(neorel.end_node.id), #self._nodeN2G(neorel.end_node),
                            **dict(neorel.items()))
            self._relationcache[neorel]=relation
        relation =  self._relationcache[neorel]
        self._uidrelationcache[relation._uid] = relation
        return relation

    def _pathN2G(self, neopath):
        path = Path()
        n0 = self._nodeN2G(neopath.start_node)

        for rel in neopath:
            relation = self._relN2G(rel)
            path.relations.append(relation)

        for n in neopath.nodes:
            path.nodes.append(self._nodeN2G(n))

        for i in range(len(path.nodes)):
            path.elements.append(path.nodes[i])
            if path.relations and i<len(path.relations):
                path.elements.append(path.relations[i])

        return path


    def query(self,query,**kwargs):
        if not self.tx:
            self.begin()
        out = Result()
        #print(query,kwargs)
        data = self.tx.run(query,**kwargs)

        for row in data:
            line = Row()
            for k,v in row.items():
                value=v
                #print(type(v))
                if type(v) == neo4j.Node:
                    value = self._nodeN2G(v)
                elif isinstance(v,neo4j.Relationship):
                    value = self._relN2G(v)
                elif isinstance(v,neo4j.Path):
                    value = self._pathN2G(v)

                line[k] = value
            out.append(line)
        return out


    def storeNode(self,node):
        q = "MERGE (n {_uid:%s}) ON CREATE SET n={props} ON MATCH SET n={props} return n" % repr(node._uid)
        props = {}
        for k,v in node.__dict__.items():
            if type(v)==set:
                v = list(v)
            props[k]=v

        r = self.query(q,props=props)
        n = r.first.n
        toremove = n._labels.difference(node._labels)
        toadd = node._labels.difference(n._labels)
        if (toremove or toadd):
            q = 'MATCH (n {_uid:%s})' % repr(n._uid)
            if toremove:
                q+= ' REMOVE n:%s ' % ':'.join(toremove)
            if toadd:
                q+= ' SET n:%s' % ':'.join(toadd)
            q += ' RETURN n'
            r = self.query(q)
            n = r.first.n
        return n

    def getNodeById(self,id):
        if id not in self._idnodecache:
            q = "MATCH (n) where id(n) = {id} return n"
            r = self.query(q,id=id)
            if r:
                self._idnodecache[id]=r.first.n
        return self._idnodecache.get(id)

    def getNode(self,_uid):
        if isinstance(_uid,Node):

            _uid = _uid._uid
        if _uid not in self._uidnodecache:
            q = "MATCH (n) where n._uid=%s return n limit 1" % repr(_uid)
            r = self.query(q)
            if r:
                self._uidnodecache[_uid] = r.first.n
        return self._uidnodecache.get(_uid)


    def findNodes(self,**kwargs):
        f = []
        for k,v in kwargs.items():
            if not isinstance(v,Filter):
                v = Filter(value=v)
            f.append(v.s(k))
        order = 'order by toInt(substring(n._uid,%s))' % (len(PREFIX))
        if f:
            q = "MATCH (n) where %s return n %s" % (' AND '.join(f),order)
        else:
            q = "MATCH (n) return n %s " % order
        r = self.query(q)
        if r:
            return [row.n for row in r]


    def jump(self,node,direction=None, reltypes=None, labels=None):
        in_arrow=''
        out_arrow=''

        if direction=='in':
            in_arrow = '<'
        elif direction=='out':
            out_arrow='>'

        q = 'MATCH (n)%s-[r]-%s(m) WHERE n._uid=%s' % (in_arrow,out_arrow,repr(node._uid))

        if reltypes:
            if type(reltypes)==str:
                reltypes = [reltypes]
            q+=' AND (' + ' OR '.join(['type(r)=%s' % repr(rt) for rt in reltypes]) +')'

        if labels:
            if type(labels)==str:
                labels = [labels]
            q+=' AND ('+ ' OR '.join(['m:%s' % l for l in labels])+')'

        q+=' RETURN n,r,m'
        r = self.query(q)
        return r




    def delNode(self,node):
        pass


    def getRelation(self,_uid):
        if isinstance(_uid,Relation):
            _uid = _uid._uid

        if _uid not in self._uidrelationcache:
            q = "MATCH ()-[r]->() where r._uid=%s return r limit 1" % repr(_uid)
            r = self.query(q)
            if r:
                self._uidrelationcache[_uid] = r.first.r
        return self._uidrelationcache.get(_uid)


    def findRelations(self,**kwargs):
        f = []
        for k,v in kwargs.items():
            if not isinstance(v,Filter):
                v = Filter(value=v)
            f.append(v.s(k))
        order = 'order by toInt(substring(r._uid,%s))' % (len(PREFIX))
        if f:
            q = "MATCH ()-[r]->() where %s return r %s" % (' AND '.join(f),order)
        else:
            q = "MATCH ()-[r]->() return r %s" % order

        r = self.query(q)
        if r:
            return [row.r for row in r]


    def dict2cypher(self,d):
        out = []
        for k,v in d.items():
            out.append('`%s`:%s' % (k,repr(v)))

        return '{'+','.join(out)+'}'

    def storeRelation(self,relation):

        # XXX is this the best place to do this?
        if not relation._source._uid in self._uidnodecache:
            self.storeNode(relation._source)
        if not relation._target._uid in self._uidnodecache:
            self.storeNode(relation._target)

        # check if there is an old one by uid
        old = self.getRelation(relation._uid)

        if old and old._reltype == relation._reltype:
            # print('updating old')
            q = "MATCH (n)-[r]->(m) where r._uid={ruid} SET r = {props} return r"
            r = self.query(q,ruid=old._uid,props=relation._getProps())
        else:
            if old:
                # print('removing old')
                q = "MATCH (n)-[r]->(m) where r._uid={ruid} DELETE r"
                r = self.query(q,ruid=old._uid)

            #print('creating new')
            q = "MATCH (n),(m) where n._uid={nuid} and m._uid={muid} CREATE (n)-[r:%s {props}]->(m) return r" % relation._reltype
            r = self.query(q,nuid=relation._source._uid,muid=relation._target._uid,props = relation._getProps())

        return r.first.r

    def delRelation(self,relation):
        pass



class Result(list):

    @property
    def first(self):
        return self[0]

class Row(dict):

    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
        self.__dict__=self

class Filter():

    def __init__(self,comparison='=',value=None):
        self.comparison = comparison
        self.value = value

    def s(self,k,nodename='n'):
        return '%s.%s %s %s' % (nodename,k,self.comparison,repr(self.value))

class Exists(Filter):

    def s(self,k,nodename='n'):
        return "EXISTS (%s.%s)" % (nodename,k)

exists = Exists()