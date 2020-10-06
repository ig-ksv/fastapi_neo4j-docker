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
                print("INFO:     Database connection is active")
            except ServiceUnavailable as e:
                time.sleep(3)
            else:
                self.db_cache_warm_up()
                print("INFO:     Database is cached")
                return

    def close_connection(self):
        self.driver.close()

    def db_cache_warm_up(self):
        with self.driver.session() as session:
            result = session.write_transaction(self._db_cache_warm_up)
        return result

    @staticmethod
    def _db_cache_warm_up(tx):
        query = f"""
                    CALL apoc.warmup.run()
                """
        result = tx.run(query)
        return result.single()[0]


neo4j_driver = DataBaseConnector("bolt://neo4j:7687", "neo4j", "test")

# CREATE (employee:Person:Employee:Production { name:'John', surname: 'Doe' })
# CREATE (employee:Person:Employee:Administration { name:'Mark', surname: 'Le' })
# CREATE (project_1:Project:Internal { name: 'FaceBook', description: '' })
# CREATE (project_2:Project:External { name: 'DropBox', description: '' })
# CREATE (aws:Skill:Hard:Technical:CloudSystem {name: 'AWS', description: ''})
# CREATE (html:Skill:Hard:Technical:MarkupLanguage {name: 'HTML', description: ''})
# CREATE (html:Skill:Hard:Technical:MarkupLanguage {name: 'XML', description: ''})
# CREATE (python:Skill:Hard:Technical:ProgramLanguage {name: 'Python', description: ''})
# CREATE (javascript:Skill:Hard:Technical:ProgramLanguage {name: 'JavaScript', description: ''})
# CREATE (java:Skill:Hard:Technical:ProgramLanguage {name: 'Java', description: ''})
# CREATE (django:Skill:Hard:Technical:WebFramework {name: 'Django', description: ''})
# CREATE (vuejs:Skill:Hard:Technical:WebFramework {name: 'VueJS', description: ''})
# CREATE (vuex:Skill:Hard:Technical:Library {name: 'Vuex', description: ''})
# CREATE (graphql:Skill:Hard:Technical:QueryLanguage {name: 'GraphQL', description: ''})
# CREATE (relay:Skill:Hard:Technical:QraphQlClientFramework {name: 'Relay', description: ''})
# CREATE (appolo:Skill:Hard:Technical:QraphQlClientFramework {name: 'Appolo', description: ''})
# CREATE (graphene:Skill:Hard:Technical:Library {name: 'Graphene', description: ''})
# CREATE (graphene_django:Skill:Hard:Technical:Library {name: 'GrapheneDjango', description: ''})
# CREATE (graphene_django)-[:BUILD_ON]->(django)
# CREATE (graphene_django)-[:BUILD_ON]->(graphene)
# CREATE (language:Skill:Hard:Language {name: 'Ukrainian', description: ''})
# CREATE (leadership:Skill:Soft {name: 'Leadership', description: ''})
# CREATE (project)-[:APPLY]->(aws)
# CREATE (project)-[:APPLY]->(python)
# CREATE (project)-[:APPLY]->(django)
# CREATE (project)-[:APPLY]->(graphene_django)
# CREATE (employee)-[:KNOW]->(python)
# CREATE (employee)-[:KNOW]->(django)
# CREATE (employee)-[:KNOW]->(graphql)
# CREATE (employee)-[:KNOW]->(graphene)
# CREATE (employee)-[:KNOW]->(graphene_django)
# CREATE (employee)-[:KNOW]->(language)
# CREATE (employee)-[:KNOW]->(leadership)
# CREATE (employee)-[:WORK_ON {start_date: '12-12-2020'}]->(project)
# CREATE (django)-[:BUILD_ON]->(python)
# CREATE (graphene)-[:BUILD_ON]->(graphql)
# CREATE (graphene)-[:BUILD_ON]->(python)
# CREATE (graphene_django)-[:BUILD_ON]->(django)
# CREATE (graphene_django)-[:BUILD_ON]->(graphene)