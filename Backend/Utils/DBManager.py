import sqlite3

# DBManager is responsible for handling the database connection
class DBManager:
    DATABASE_PATH = ""

    # Constructor to handle custom initilization
    def __init__(self):
        """
        Initialize the DBManager and connect to the database using the class-level path.

        This constructor sets up a persistent connection to the database and ensures
        the table is created if it doesn't already exist.
        """
        if not DBManager.DATABASE_PATH:
            raise ValueError("DATABASE_PATH must be set before initializing DBManager.")
        
        # Establish the connection using the class-level DATABASE_PATH
        self.connection = sqlite3.connect(DBManager.DATABASE_PATH)
        self.CreateTableIfNotExists()

    def CreateTableIfNotExists(self):
        """
        Ensure that the 'values' table exists in the database.

        This is only run once during initialization and will create the table if missing.
        """
        create_table_query = """
            CREATE TABLE IF NOT EXISTS values (
                ValueId INTEGER PRIMARY KEY AUTOINCREMENT,
                Name TEXT NOT NULL,
                Key TEXT NOT NULL
            )
        """
        self.connection.execute(create_table_query)
        self.connection.commit()

    def CreateValue(self, value):
        """
        Create a new record in the database.

        Parameters:
            value (Value): A Value object. The 'id' property is ignored during creation.

        Returns:
            int: The ID of the newly created record.
        """
        insert_query = "INSERT INTO values (Name, Key) VALUES (?, ?)"
        cursor = self.connection.execute(insert_query, (value.name, value.key))
        self.connection.commit()
        new_id = cursor.lastrowid  # Fetch auto-generated ID
        return new_id

    def SaveValue(self, value):
        """
        Update an existing record in the database.

        Parameters:
            value (Value): A Value object with a valid ValueId, Name, and Key.

        Returns:
            bool: True if the update was successful, False otherwise.
        """
        update_query = "UPDATE values SET Name = ?, Key = ? WHERE id = ?"
        cursor = self.connection.execute(update_query, (value.name, value.key, value.id))
        self.connection.commit()
        return cursor.rowcount > 0  # True if at least one row was updated

    def DeleteValue(self, value):
        """
        Delete an existing record from the database.

        Parameters:
            value (Value): A Value object with a valid id.

        Returns:
            bool: True if the deletion was successful, False otherwise.
        """
        delete_query = "DELETE FROM values WHERE ValueId = ?"
        cursor = self.connection.execute(delete_query, (value.id,))
        self.connection.commit()
        return cursor.rowcount > 0  # True if at least one row was deleted