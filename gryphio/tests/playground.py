from pprint import pprint

from neo4jdb import Neo4jDB, Filter, exists
from graph import *
from config import auth
db = Neo4jDB(*auth)
graph = Graph(db)
r = db.query('match p=(n)-[r]->(m)-[r2]->(n) return p,n,m,[n,m] as foo')
row = r[0]
p = row.p
print(p)
n = p.nodes[0]

n2 = db.getNode('meta17')
n2._labels.add('foobar')
n2._labels.add('foobar2')
#n2._labels.remove('Person')
n3 = db.storeNode(n2)
print(n2 == n == n3)
print(n)
print(n2)
print(n3)





alice=graph.getNode('meta17')
bob=graph.getNode('meta16')
#graph.jump(person,'out',['M_N_PROP','bar'],'M_Property')

person = graph.getSchema('Person')
print('person?',repr(person))
print(person.checkNode(alice))
print(person.getPropKeys())

newnode = graph.storeNode(Node())
print(newnode)
person.assignTo(newnode)
print(newnode)

schema =graph.getSchema('_Schema')
print(schema)


s2 = graph.getSchema(_schemaname='_Schema')
print(s2)

# print()
# for node in graph.allNodes():
#     print(node)
#     print(graph.checkSchemas(node))

print (graph.maxArity(alice,'name'))
s3 = graph.getSchema(_techname='LIKES')
print(s3)


graph.db.rollback()
print()

#print(s2.checkNode(s2))
#print(graph.getRelation('meta35'))
#print()
#print(graph.exportCypher(detach=1))
# for n in graph.findNodes(_schemaname=Exists()):
#     s2.assignTo(n)

n5 = Node('Test',name='n5')
n6 = Node('Test',name='n6')

r = Relation(n5,'testrel',n6,foo='bar')
print(r.__dict__)
r2 = graph.storeRelation(r)
print(r2.__dict__)
graph.storeRelation(r)
r._reltype='newrel'
graph.storeRelation(r)
person.assignTo(r)

likes = graph.findNodes(_techname='LIKES')[0]
print(graph.allowedSourceSchemas(likes))
print(graph.allowedTargetSchemas(likes))

print(graph.relationPossible(alice,'LIKES',bob))

p1 = Node()
person.assignTo(p1)
graph.storeNode(p1)
p2 = Node()
person.assignTo(p2)
graph.storeNode(p2)
print('p1->p2',graph.relationPossible(p1,'LIKES',p2))
r3 = Relation(p1,'LIKES',p2)
graph.storeRelation(r3)
print('p1->p2',graph.relationPossible(p1,'LIKES',p2))
p3 = Node()
person.assignTo(p3)
graph.storeNode(p3)
print('p3->p2',graph.relationPossible(p3,'LIKES',p2))
