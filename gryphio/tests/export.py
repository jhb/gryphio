from neo4jdb import Neo4jDB
from graph import *
from config import auth
db = Neo4jDB(*auth)
graph = Graph(db)

print(graph.exportCypher(detach=1))