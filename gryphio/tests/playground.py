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

n2 = db.getNode('m17')
n2._labels.add('foobar')
n2._labels.add('foobar2')
n2._labels.remove('Person')
n3 = db.storeNode(n2)
print(n2 == n == n3)
print(n)
print(n2)
print(n3)

person = db.getNode('m12')



alice=graph.getNode('m17')
person = graph.getNode('m12')
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

print()
for node in graph.allNodes():
    print(node)
    print(graph.checkSchemas(node))


graph.db.rollback()
print()

#print(s2.checkNode(s2))
#print(graph.getRelation('m35'))
#print(graph.exportCypher(detach=1))
# for n in graph.findNodes(_schemaname=Exists()):
#     s2.assignTo(n)