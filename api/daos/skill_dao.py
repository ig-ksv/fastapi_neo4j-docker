import uuid

from api.daos.db_connector import neo4j_driver
from api.models.skill import SKillOut, SKillIn, get_label_type


class SkillDAO:
    def add_skill(self, skill: SKillIn):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._add_and_return_skill, skill)
        return result

    @staticmethod
    def _add_and_return_skill(tx, skill: SKillIn):
        labels = [x for x in skill.labels.values()]
        labels = ":".join(labels)
        custom_id = uuid.uuid4()
        query = f"""
                    CREATE (e:Skill:{labels}) 
                    SET e.name = '{skill.name}' 
                    SET e.description = '{skill.description}'
                    SET e.custom_id = '{custom_id}'
                    RETURN e
                """
        result = tx.run(query)
        skill = result.single()[0]
        result = dict(skill.items())
        result["labels"] = {get_label_type(label): label for label in list(skill.labels)}
        return result

    def delete_skill(self, custom_id):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._delete_skill, custom_id)
        return result

    @staticmethod
    def _delete_skill(tx, custom_id):
        query = f"""
                    MATCH (e:Skill)
                    WHERE e.custom_id = '{custom_id}'
                    detach delete e
                """
        result = tx.run(query)
        return result

    def get_skills(self, params):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._get_skills, params)
        return result

    @staticmethod
    def _get_skills(tx, params):
        name = params.get("name")
        clause = ""
        if params.get("name"):
            clause = f"WHERE e.name = '{name}'"
        labels = ""
        if params.get("labels"):
            print(params.get("labels"))
            labels = ":" + ":".join(params.get("labels"))
        query = f"""
                    MATCH (e:Skill{labels})
                    {clause}
                    RETURN e
                """
        print(query)
        result = tx.run(query)
        result = result.value()
        items = [dict(node.items()) for node in result]
        for index, node in enumerate(result):
            items[index]["labels"] = {get_label_type(label): label for label in list(node.labels)}
        return items

    def upload_bulk_csv(self, file_name: str):
        with neo4j_driver.driver.session() as session:
            result = session.write_transaction(self._upload_bulk_csv, file_name)
        return result

    @staticmethod
    def _upload_bulk_csv(tx, file_name: str):
        query = f"""
                    CALL apoc.load.csv('{file_name}', {{sep: '|', mapping:{{LABELS: {{array:true, arraySep:','}}}}}}) YIELD map
                    CALL apoc.merge.node(['SKILL'] + map.LABELS, {{name: map.name}}, 
                                         {{custom_id: map.custom_id, 
                                           name: map.name, 
                                           description: map.description}}) YIELD node
                    RETURN count(*) as number
                 """
        try:
            result = tx.run(query)
        except Exception as e:
            raise Exception(f"Import failed -{e}")
        else:
            return f"Data has been successfully loaded - {result.single()['number']} rows"

