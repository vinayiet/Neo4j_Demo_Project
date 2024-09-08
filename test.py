import logging
from neo4j import GraphDatabase, RoutingControl
from neo4j.exceptions import DriverError, Neo4jError

logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

class SocialNetworkApp:
    def __init__(self, uri, user, password, database=None):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database

    def close(self):
        self.driver.close()

    def create_users(self, usernames):
        with self.driver.session() as session:
            for username in usernames:
                try:
                    result = session.write_transaction(self._create_user, username)
                    logging.info("Created user: %s", result["username"])
                except Exception as e:
                    logging.error("Failed to create user: %s", e)

    def _create_user(self, tx, username):
        query = "MERGE (u:User { username: $username }) RETURN u.username AS username"
        result = tx.run(query, username=username)
        return result.single()

    def create_friendships(self, friendships):
        with self.driver.session() as session:
            for user1, user2 in friendships:
                try:
                    result = session.write_transaction(self._create_friendship, user1, user2)
                    logging.info("Created friendship between: %s and %s", result["user1"], result["user2"])
                except Exception as e:
                    logging.error("Failed to create friendship: %s", e)

    def _create_friendship(self, tx, user1, user2):
        query = (
            "MATCH (u1:User { username: $user1 }), (u2:User { username: $user2 }) "
            "MERGE (u1)-[:FRIENDS_WITH]->(u2) "
            "RETURN u1.username AS user1, u2.username AS user2"
        )
        result = tx.run(query, user1=user1, user2=user2)
        return result.single()

    def list_friends(self, usernames):
        with self.driver.session() as session:
            for username in usernames:
                try:
                    friends = session.read_transaction(self._list_friends, username)
                    logging.info("Friends of %s: %s", username, friends)
                except Exception as e:
                    logging.error("Failed to list friends for %s: %s", username, e)

    def _list_friends(self, tx, username):
        query = (
            "MATCH (u:User { username: $username })-[:FRIENDS_WITH]->(friend) "
            "RETURN friend.username AS friend ORDER BY friend.username"
        )
        result = tx.run(query, username=username)
        return [record["friend"] for record in result]

    def remove_friendships(self, friendships):
        with self.driver.session() as session:
            for user1, user2 in friendships:
                try:
                    result = session.write_transaction(self._remove_friendship, user1, user2)
                    logging.info("Removed friendship between: %s and %s", result["user1"], result["user2"])
                except Exception as e:
                    logging.error("Failed to remove friendship: %s", e)

    def _remove_friendship(self, tx, user1, user2):
        query = (
            "MATCH (u1:User { username: $user1 })-[:FRIENDS_WITH]->(u2:User { username: $user2 }) "
            "DELETE u1-[:FRIENDS_WITH]->u2 "
            "RETURN u1.username AS user1, u2.username AS user2"
        )
        result = tx.run(query, user1=user1, user2=user2)
        return result.single()

if __name__ == "__main__":
    # Configuration
    scheme = "neo4j+s"  # Use the appropriate scheme
    host_name = "450291b0.databases.neo4j.io"  # Replace with your actual host
    port = 7687
    uri = f"{scheme}://{host_name}:{port}"
    user = "neo4j"
    password = "Tn9Z2IprOaKzlSS7YxJS-PkxFWzKl0OIroxkXBmc44Y"
    database = "neo4j"
    
    # Initialize the application
    app = SocialNetworkApp(uri, user, password, database)
    
    try:
        # Create multiple users
        app.create_users(["Alice", "Bob", "Charlie", "David", "Eve"])
        
        # Create multiple friendships
        app.create_friendships([
            ("Alice", "Bob"),
            ("Alice", "Charlie"),
            ("Bob", "David"),
            ("Charlie", "Eve")
        ])
        
        # List friends for multiple users
        app.list_friends(["Alice", "Bob", "Charlie"])
        
        # Remove multiple friendships
        app.remove_friendships([
            ("Alice", "Charlie"),
            ("Bob", "David")
        ])
        
        # List friends after removal
        app.list_friends(["Alice", "Bob", "Charlie"])
    finally:
        app.close()
