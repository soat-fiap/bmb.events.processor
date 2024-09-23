from neo4j import GraphDatabase

class Neo4jGateway:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        
    def get_driver(self):
        return self.driver