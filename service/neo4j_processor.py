import logging
from neo4j import GraphDatabase
from neo4j.exceptions import ServiceUnavailable


class App:

    def __init__(self, uri, user, password):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))

    def close(self):
        self.driver.close()

    def create_friendship(self, person1_name, person2_name):
        with self.driver.session() as session:
            result = session.write_transaction(
                self._create_and_return_friendship, person1_name, person2_name)
            for record in result:
                print("Created friendship between: {p1}, {p2}".format(
                    p1=record['p1'], p2=record['p2']))

    @staticmethod
    def _create_and_return_friendship(tx, person1_name, person2_name):
        query = (
            "CREATE (p1:Person { name: $person1_name }) "
            "CREATE (p2:Person { name: $person2_name }) "
            "CREATE (p1)-[:KNOWS]->(p2) "
            "RETURN p1, p2"
        )
        result = tx.run(query, person1_name=person1_name, person2_name=person2_name)
        try:
            return [{"p1": record["p1"]["name"], "p2": record["p2"]["name"]}
                    for record in result]
        except ServiceUnavailable as exception:
            logging.error("{query} raised an error: \n {exception}".format(
                query=query, exception=exception))
            raise

    def get_friends_of(self, person_name):
        with self.driver.session() as session:
            result = session.read_transaction(self._get_and_return_friends_of, person_name)
            for record in result:
                print("Found person: {record}".format(record=record))

    @staticmethod
    def _get_and_return_friends_of(tx, name):
        friends = []
        query = (
            "MATCH (a:Person)-[:KNOWS]->(f) "
            "WHERE a.name = $name "
            "RETURN f.name AS friend"
        )
        result = tx.run(query, name=name)
        for record in result:
            friends.append(record["friend"])
        return friends


if __name__ == "__main__":
    scheme = "neo4j"
    host_name = "localhost"
    port = 7687
    url = "{scheme}://{host_name}:{port}".format(scheme=scheme, host_name=host_name, port=port)
    user = "neo4j"
    password = "test"
    app = App(url, user, password)
    app.create_friendship("Alice", "Barbara")
    app.create_friendship("Alice", "Carlos")
    app.create_friendship("Alice", "David")
    app.create_friendship("Carlos", "David")
    app.get_friends_of("Alice")
    app.close()