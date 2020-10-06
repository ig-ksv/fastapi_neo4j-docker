import uuid

from api.daos.db_connector import neo4j_driver


class RelationshipDAO:
    def add_relationship(self, relationship):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._add_relationship, relationship)
        return result

    @staticmethod
    def _add_relationship(tx, relationship):
        custom_id = uuid.uuid4()
        start_node_labels = ""
        if relationship.start_node_labels:
            start_node_labels = ":" + ":".join(relationship.start_node_labels)

        end_node_labels = ""
        if relationship.end_node_labels:
            end_node_labels = ":" + ":".join(relationship.end_node_labels)

        query = f"""
                    MATCH (p{start_node_labels} {{custom_id: '{relationship.start_node_id}'}}), 
                          (s{end_node_labels} {{custom_id: '{relationship.end_node_id}'}})
                    CREATE (p)-[r:{relationship.name}]->(s)
                    SET r.custom_id = '{custom_id}'
                    RETURN r
                """
        result = tx.run(query)
        result = result.single()
        if len(result) > 0:
            result = result[0]
            return result
        return "No id match"

    def upload_bulk_csv(self, file_name: str):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._upload_bulk_csv, file_name)
        return result

    @staticmethod
    def _upload_bulk_csv(tx, file_name: str):
        query = f"""
                    CALL apoc.load.csv('{file_name}', {{sep: '|'}}) YIELD map
                    MATCH (n1) WITH n1, map
                    MATCH (n2)
                    WHERE n1.custom_id = map.start_node_id AND n2.custom_id = map.end_node_id
                    CALL apoc.create.relationship(n1, map.role, {{}}, n2) YIELD rel
                    RETURN count(*) as number
                 """
        print(query)
        try:
            result = tx.run(query)
        except Exception as e:
            raise Exception(f"Import failed -{e}")
        else:
            return f"Data has been successfully loaded - {result.single()['number']} rows"

