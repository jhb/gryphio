import neo4j
import json
from tools import searchkeys


class NeoDB:

    def __init__(self, uri, login, passwd):
        self.driver = neo4j.GraphDatabase.driver(uri, auth=(login, passwd))
        self.session = self.driver.session()
        self.tx = None

        self.searchkeys = searchkeys

    def begin(self):
        self.tx = self.session.begin_transaction()
        return self.tx

    def commit(self):
        self.tx.commit()
        self.tx = None

    def rollback(self):
        self.tx.rollback()
        self.tx = None

    def run(self, stmt, *args, **kwargs):
        if not self.tx:
            self.begin()
        return self.tx.run(stmt, **kwargs)

    def getType(self, value):
        if isinstance(value, neo4j.Node):
            return 'node'
        elif isinstance(value, neo4j.Relationship):
            return 'edge'
        elif isinstance(value, neo4j.Path):
            return 'path'
        else:
            return 'other'

    def getResult(self, query):
        result = self.run(query)
        return result

    def graphJSON(self, query, complete=True):
        result = self.getResult(query)
        if complete:
            nodeids = [n.id for n in result.graph().nodes]
            query = 'match p=(n)-[r]->(m) where id(n) in {nodeids} and id(m) in {nodeids} return p'
            result = self.run(query, nodeids=nodeids)

        graph = result.graph()
        nodes = []
        for node in graph.nodes:
            labels = list(node.labels)
            nodes.append(dict(id=str(node.id),
                              name=self.searchkeys(node, 'shortname', 'name', 'vorname', ''),
                              label=len(labels) and labels[0] or ''
                              ), )
        links = []
        for edge in graph.relationships:
            links.append(dict(id=edge.id,
                              source=str(edge.start_node.id),
                              target=str(edge.end_node.id),
                              name=edge.type,
                              ))
        return json.dumps(dict(nodes=nodes, links=links))

    def getNode(self, nodeid):
        nodeid = int(nodeid)
        result = self.run('match (n) where id(n) = {nodeid} return n', nodeid=nodeid)
        return result.single()['n']
