Social Network Application with Neo4j and Python
Overview
This project is a Python-based Social Network Application that utilizes Neo4j, a graph database, to manage user profiles and their relationships. The application demonstrates how to create multiple users, establish friendships, list friends, and remove friendships using Neo4j's graph database capabilities in conjunction with Python.

Features
Create Multiple Users: Add multiple user profiles to the Neo4j database.
Create Multiple Friendships: Establish FRIENDS_WITH relationships between multiple users.
List Friends for Multiple Users: Retrieve and display friends for specified users.
Remove Multiple Friendships: Delete FRIENDS_WITH relationships between specified users.
Prerequisites
Neo4j Database: Ensure you have access to a Neo4j database instance. You will need the connection URI, username, and password.
Python: Python should be installed on your system. It is recommended to use a virtual environment.
Python Packages: The neo4j Python package is required. Install it using pip.
bash
Copy code
pip install neo4j
Project Structure
social_network_app.py: Main application code for creating users, managing friendships, and interacting with the Neo4j database.
requirements.txt: Lists the required Python packages for the project.
Code Explanation
Import Statements
python
Copy code
import logging
from neo4j import GraphDatabase, RoutingControl
from neo4j.exceptions import DriverError, Neo4jError
logging: For logging errors and information.
GraphDatabase: To interact with the Neo4j database.
RoutingControl: For managing query routing.
DriverError, Neo4jError: For handling Neo4j exceptions.
SocialNetworkApp Class
Initialization
python
Copy code
class SocialNetworkApp:
    def __init__(self, uri, user, password, database=None):
        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self.database = database
Initializes the Neo4j driver and database connection.
Closing the Connection
python
Copy code
    def close(self):
        self.driver.close()
Closes the Neo4j driver connection.
Creating Users
python
Copy code
    def create_users(self, usernames):
        with self.driver.session() as session:
            for username in usernames:
                try:
                    result = session.write_transaction(self._create_user, username)
                    logging.info("Created user: %s", result["username"])
                except Exception as e:
                    logging.error("Failed to create user: %s", e)
Creates user profiles in the database.
Creating Friendships
python
Copy code
    def create_friendships(self, friendships):
        with self.driver.session() as session:
            for user1, user2 in friendships:
                try:
                    result = session.write_transaction(self._create_friendship, user1, user2)
                    logging.info("Created friendship between: %s and %s", result["user1"], result["user2"])
                except Exception as e:
                    logging.error("Failed to create friendship: %s", e)
Establishes FRIENDS_WITH relationships between users.
Listing Friends
python
Copy code
    def list_friends(self, usernames):
        with self.driver.session() as session:
            for username in usernames:
                try:
                    friends = session.read_transaction(self._list_friends, username)
                    logging.info("Friends of %s: %s", username, friends)
                except Exception as e:
                    logging.error("Failed to list friends for %s: %s", username, e)
Retrieves and displays friends for specified users.
Removing Friendships
python
Copy code
    def remove_friendships(self, friendships):
        with self.driver.session() as session:
            for user1, user2 in friendships:
                try:
                    result = session.write_transaction(self._remove_friendship, user1, user2)
                    logging.info("Removed friendship between: %s and %s", result["user1"], result["user2"])
                except Exception as e:
                    logging.error("Failed to remove friendship: %s", e)
Removes FRIENDS_WITH relationships between users.
Main Execution
python
Copy code
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
Initializes and demonstrates the functionality of the SocialNetworkApp class.
Usage
Configure the Connection:

Update the scheme, host_name, port, user, password, and database with your Neo4j instance details.
Run the Application:

Execute the script using Python to perform operations like creating users, establishing friendships, listing friends, and removing friendships.
Check Logs:

Review the logs for information on operations performed and any errors encountered.
