from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable
import time


class DataBaseConnector:
    def __init__(self, uri, username, password):
        self.uri = uri
        self.username = username
        self.password = password
        self.driver = None

    def open_connection(self):
        while True:
            try:
                self.driver = GraphDatabase.driver(self.uri, auth=(self.username, self.password))
                print("Success - database connection is active")
                return
            except ServiceUnavailable as e:
                time.sleep(2)
                print(e)

    def close_connection(self):
        self.driver.close()


neo4j_driver = DataBaseConnector("bolt://neo4j:7687", "neo4j", "test")