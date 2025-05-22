# Class to save all local settings for the program
class ProgramSettings:
    DEFAULT_CRYPT_KEY = "?l4![e_-_~:[C8oZO#Y3K,z53Mb$#2x6"  # Used for db table 'saves'
    DATABASE_PATH = "app_database.db"                       # Name of the database
    CRYPT_KEY = DEFAULT_CRYPT_KEY                           # Set to the default crypt key to avoid errors with empty crypt_key while initilization