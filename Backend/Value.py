# Each Value has an id, a name, and a key.
class Value:
    # Constructor to handle custom initilization
    def __init__(self, id, name, key):
        """
        Initialize the Value object.
        
        Parameters:
            id (int): The unique identifier for the value record.
            name (str): The name of the value.
            key (str): The key associated with the value.
        """
        self.id = id
        self.name = name
        self.key = key