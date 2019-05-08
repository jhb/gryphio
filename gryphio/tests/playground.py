from gryphio.neo4jdb import Neo4jDB, Filter, exists
from gryphio.graph import *
from gryphio.config import auth
db = Neo4jDB(*auth)
r = db.query('match p=(n)-[r]->(m)-[r2]->(n) return p,n,m,[n,m] as foo')
row = r[0]
p = row.p
print(p)
n = p.nodes[0]

n2 = db.getNode('sem17')
n2._labels.add('foobar')
n2._labels.add('foobar2')
n2._labels.remove('Person')
n3 = db.storeNode(n2)
print(n2 == n == n3)
print(n)
print(n2)
print(n3)

person = db.getNode('sem12')


graph = Graph(db)
alice=graph.getNode('sem17')
person = graph.getNode('sem12')
#graph.jump(person,'out',['Sem_N_PROP','bar'],'Sem_Property')

schema = graph.getSchema('sem12')
print(schema)
print(schema.checkNode(alice))
print(schema.getPropKeys())

newnode = graph.storeNode(Node())
print(newnode)
schema.assignTo(newnode)
print(newnode)

schema =graph.getSchema('sem1')
print(schema)

n4 = graph.findNodes(_schemaname=exists)
print(n4)
s2 = graph.getSchema(graph.findNodes(_schemaname='Schema')[0])
print(s2)

# for n in graph.findNodes(_schemaname=Exists()):
#     s2.assignTo(n)