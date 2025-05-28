from Backend.Utils.DBManager import DBManager
from Backend.Utils.Encryption import Encryption
from Backend.ProgramSettings import ProgramSettings

# Class to handle helping functions
class ToolHelper:
    """
    A helper class that provides some functions for managing
    "A class to store functions"
    """

    def __init__(self, db: DBManager, encryption: Encryption):
        """
        Initializes the ToolHelper with references to the database manager and encryption handler.

        Args:
            db (DBManager): The database manager instance for performing database operations.
            encryption (Encryption): The encryption instance for encrypting and decrypting values.
        """

        self.db = db
        self.encryption = encryption

    def UpdateUserPassword(self, new_user_password: str) -> bool:
        """
        Updates the user's password and re-encrypts all saved values using the new password.

        This method:
        1. Sets the encryption key to the default to read the existing password.
        2. Encrypts the new user password and updates it in the 'saves' table.
        3. Decrypts the old password and re-encrypts all saved values using the new password.

        Args:
            new_user_password (str): The new password provided by the user.

        Returns:
            bool: True if password update and re-encryption process completed, False otherwise.
        """

        # Set crypt_key to default (default is used for 'saved' table in db)
        ProgramSettings.CRYPT_KEY = ProgramSettings.DEFAULT_CRYPT_KEY
        # Encrypt new user password
        new_user_password_encrypted = self.encryption.Encrypt(new_user_password)
        # Get old user password from database
        old_user_password_encrypted = self.db.tableSaves_GetSave(1)
        # Decrypt old user password
        old_user_password = self.encryption.Decrypt(old_user_password_encrypted)
        # Update new user password in database with encrypted password
        self.db.tableSaves_UpdateSave(1, "user", new_user_password_encrypted)
        # Recrypt all values in database table 'values' with new user password
        return self.RecryptValues(old_user_password, new_user_password)

    def RecryptValues(self, crypt_key_old, crypt_key_new) -> bool:
        """
        Re-encrypts all values in the database using a new encryption key.

        This method:
        1. Decrypts each stored value using the old password.
        2. Re-encrypts it using the new password.
        3. Updates the encrypted value back in the database.

        Args:
            crypt_key_old (str): The current password used to decrypt values.
            crypt_key_new (str): The new password to encrypt values with.

        Returns:
            bool: True if all values were successfully re-encrypted, False otherwise.
        """

        all_values = self.db.tableValues_GetAllValues()
        for name, key in all_values:
            # Decrypt key with old crypt key
            ProgramSettings.CRYPT_KEY = crypt_key_old
            decrypted_key = self.encryption.Decrypt(key)

            # Encrypt key with new crypt key
            ProgramSettings.CRYPT_KEY = crypt_key_new
            encrypted_key = self.encryption.Encrypt(decrypted_key)

            # Update value in db
            self.db.tableValues_SaveValue(name, encrypted_key)
        # Ensure crypt key is set to new user password
        ProgramSettings.CRYPT_KEY = crypt_key_new
        return True
    
    def GetDecryptedPWList(self) -> list[tuple]:
        """
        Retrieves all stored (site, encrypted_password) pairs from the database,
        decrypts each password using the current encryption key, and returns
        a list of (site, decrypted_password) tuples.

        Returns:
            list[tuple]: A list of tuples where each tuple contains:
                - site (str): The site name.
                - decrypted_password (str): The decrypted password for that site.
        """
        encrypted_value_list = self.db.tableValues_GetAllValues()
        return [
            (name, self.encryption.Decrypt(key))
            for name, key in encrypted_value_list
        ]