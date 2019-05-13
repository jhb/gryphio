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

schema =graph.getSchema('Schema')
print(schema)


s2 = graph.getSchema(_schemaname='Schema')
print(s2)

graph.db.rollback()

print()
schemas = []
for sn in graph.findNodes(_schemaname=exists):
    schema = graph.getSchema(sn)
    schemas.append(schema)
    print(schema)
print()
# for row in graph.db.query('Match (n) return n,id(n) as nid'):
#     n = row.n
#     nid = row.nid
#     print(n)
#     print(nid)
#     for schema in schemas:
#         if schema.checkNode(n):
#            print(' ',schema._schemaname)
#     print()
print(s2.checkNode(s2))
print(graph.getRelation('m35'))
print(graph.exportCypher(detach=1))
# for n in graph.findNodes(_schemaname=Exists()):
#     s2.assignTo(n)