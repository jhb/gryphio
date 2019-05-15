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
n2._labels.remove('Person')
n3 = db.storeNode(n2)
print(n2 == n == n3)
print(n)
print(n2)
print(n3)

person = db.getNode('meta12')



alice=graph.getNode('meta17')
person = graph.getNode('meta12')
#graph.jump(person,'out',['M_N_PROP','bar'],'M_Property')

schema = graph.getSchema('Person')
print(schema)
print(schema.checkNode(alice))
print(schema.getPropKeys())

newnode = graph.storeNode(Node())
print(newnode)
schema.assignTo(newnode)
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
