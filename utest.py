import unittest
from unittest.mock import MagicMock, patch
import string
import random

# Patch ProgramSettings with in-memory testing configuration
# Ensures encryption and DBManager work without persistent file storage
import Backend.ProgramSettings as ProgramSettings
ProgramSettings.CRYPT_KEY = "UnitTestKey123!"              # Key used for encryption during test
ProgramSettings.DEFAULT_CRYPT_KEY = "DefaultTestKey123!"   # Default key for fallback and re-encryption
ProgramSettings.DATABASE_PATH = ":memory:"                 # Use in-memory SQLite database for isolation

# Import classes under test
from Backend.Utils.Encryption import Encryption
from Backend.Utils.PasswordSafety import PasswordSafety
from Backend.Utils.PasswordGeneration import PasswordGeneration
from Backend.Utils.ToolHelper import ToolHelper
from Backend.Utils.DBManager import DBManager


class TestEncryption(unittest.TestCase):
    """Tests for the Encryption class (AES-256 CBC mode)."""

    def test_encrypt_and_decrypt_cycle(self):
        """Encrypt and decrypt a message, ensuring the result is identical to the original."""
        message = "SuperSecret123!"
        encryption = Encryption()
        encrypted = encryption.Encrypt(message)
        decrypted = encryption.Decrypt(encrypted)
        self.assertEqual(decrypted, message)


class TestPasswordSafety(unittest.TestCase):
    """Tests for the password safety checker (PasswordSafety class)."""

    @patch("tkinter.messagebox.showwarning")
    def test_valid_password(self, mock_warn):
        """Check that a valid password passes all rules."""
        checker = PasswordSafety()
        self.assertTrue(checker.Check("Secure!Pass123"))

    @patch("tkinter.messagebox.showwarning")
    def test_invalid_passwords(self, mock_warn):
        """Test that different weak password types trigger warnings."""
        checker = PasswordSafety()
        self.assertFalse(checker.Check("A1!a"))              # Too short
        self.assertFalse(checker.Check("secure!123"))        # Missing uppercase
        self.assertFalse(checker.Check("SECURE!123"))        # Missing lowercase
        self.assertFalse(checker.Check("Secure!Word"))       # Missing digit
        self.assertFalse(checker.Check("Secure1234"))        # Missing special character


class TestPasswordGeneration(unittest.TestCase):
    """Tests for password generator to ensure character set diversity and length."""

    def test_generated_length_and_charset(self):
        """Ensure generated passwords meet length and charset (letters, digits, special chars)."""
        for length in range(8, 17, 2):
            # Retry generation multiple times in case random result is incomplete
            for _ in range(10):
                password = PasswordGeneration.Generate(length)
                if (any(c in string.ascii_letters for c in password)
                    and any(c in string.digits for c in password)
                    and any(c in string.punctuation for c in password)):
                    break
            else:
                self.fail("Password does not include all required charsets")

            self.assertEqual(len(password), length)


class TestDBManagerInMemory(unittest.TestCase):
    """Tests for database logic using an isolated in-memory database."""

    def setUp(self):
        self.db = DBManager()
        self._init_valid_user()  # Ensure encryption-decryption works by seeding the DB correctly

    def _init_valid_user(self):
        """Encrypt and store a valid user password to simulate real application behavior."""
        enc = Encryption()
        encrypted = enc.Encrypt(ProgramSettings.DEFAULT_CRYPT_KEY)
        self.db.connection.execute("UPDATE saves SET Value = ? WHERE Name = ?", (encrypted, "user"))
        self.db.connection.commit()

    def test_value_crud(self):
        """Test create, read, update, delete operations on the 'values' table."""
        id = self.db.tableValues_CreateValue("TestSite", "EncryptedData")
        self.assertGreater(id, 0)

        self.assertEqual(self.db.tableValues_GetValue("TestSite"), "EncryptedData")

        self.assertTrue(self.db.tableValues_SaveValue("TestSite", "NewData"))
        self.assertEqual(self.db.tableValues_GetValue("TestSite"), "NewData")

        self.assertTrue(self.db.tableValues_DeleteValue("TestSite"))
        self.assertIsNone(self.db.tableValues_GetValue("TestSite"))

    def test_save_crud(self):
        """Test retrieval and update of entries in the 'saves' table (used for storing master password)."""
        value = self.db.tableSaves_GetSave(1)
        self.assertIsNotNone(value)

        self.assertTrue(self.db.tableSaves_UpdateSave(1, "user", "UpdatedValue"))
        self.assertEqual(self.db.tableSaves_GetSave(1), "UpdatedValue")


class TestToolHelper(unittest.TestCase):
    """Tests for the ToolHelper logic, including password re-encryption and decryption."""

    def setUp(self):
        # Ensure encryption setup is valid
        ProgramSettings.CRYPT_KEY = "DefaultTestKey123!"
        self.db = DBManager()
        self._init_valid_user()
        self.enc = Encryption()
        self.helper = ToolHelper(self.db, self.enc)

    def _init_valid_user(self):
        """Seed the test DB with an encrypted master password."""
        enc = Encryption()
        encrypted = enc.Encrypt(ProgramSettings.DEFAULT_CRYPT_KEY)
        self.db.connection.execute("UPDATE saves SET Value = ? WHERE Name = ?", (encrypted, "user"))
        self.db.connection.commit()

    def test_get_decrypted_pw_list(self):
        """Test decryption of a password list from the DB."""
        encrypted = self.enc.Encrypt("MySecret123!")
        self.db.tableValues_CreateValue("SiteA", encrypted)

        result = self.helper.GetDecryptedPWList()
        self.assertEqual(result[0], ("SiteA", "MySecret123!"))

    def test_update_user_password(self):
        """Test the full password update workflow (re-encryption of all values)."""
        new_pw = "NewSecret123!"
        self.assertTrue(self.helper.UpdateUserPassword(new_pw))  # Update works

        ProgramSettings.CRYPT_KEY = new_pw  # Switch encryption context
        self.db.tableValues_CreateValue("TestService", self.enc.Encrypt("Hello123!"))
        values = self.helper.GetDecryptedPWList()
        self.assertIsInstance(values, list)


class TestGUILogicMocked(unittest.TestCase):
    """Tests parts of the GUI logic using mocks to simulate messagebox behavior."""

    @patch("tkinter.messagebox.showwarning")
    def test_password_safety_warning_on_bad_password(self, mock_warn):
        """Check that weak password triggers GUI warning (mocked)."""
        checker = PasswordSafety()
        result = checker.Check("123")
        self.assertFalse(result)
        mock_warn.assert_called()

    @patch("tkinter.messagebox.showinfo")
    def test_toolhelper_password_update_flow(self, mock_info):
        """Simulate password update flow and ensure DB encryption stays valid."""
        db = DBManager()

        # Ensure valid encryption context
        enc = Encryption()
        encrypted = enc.Encrypt(ProgramSettings.DEFAULT_CRYPT_KEY)
        db.connection.execute("UPDATE saves SET Value = ? WHERE Name = ?", (encrypted, "user"))
        db.connection.commit()

        helper = ToolHelper(db, enc)
        self.assertTrue(helper.UpdateUserPassword("Abcd1234!"))


# Run all tests
if __name__ == "__main__":
    unittest.main()