from Backend.Utils.DBManager import DBManager
from Backend.Utils.Encryption import Encryption
from Backend.Utils.ToolHelper import ToolHelper
from Backend.Utils.PasswordSafety import PasswordSafety
from Backend.Utils.PasswordGeneration import PasswordGeneration
from Backend.ProgramSettings import ProgramSettings
from GUI import GUI

# Program initilization
db = DBManager()
encryption = Encryption()
ProgramSettings.CRYPT_KEY = ProgramSettings.DEFAULT_CRYPT_KEY   # Update setting to ensure crypt key is set to default
toolHelper = ToolHelper(db, encryption)
passwordSafety = PasswordSafety()
passwordGeneration = PasswordGeneration()

# Create gui
GUI(db, encryption, toolHelper, passwordSafety, passwordGeneration)