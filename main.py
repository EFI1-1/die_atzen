from Backend.Utils.DBManager import DBManager
from Backend.Utils.Encryption import Encryption
from Backend.Utils.ToolHelper import ToolHelper
from Backend.Value import Value
from Backend.ProgramSettings import ProgramSettings
from GUI import GUI

entered_password = "passwort"

# Program initilization
db = DBManager()
encryption = Encryption()

# Update settings
ProgramSettings.CRYPT_KEY = ProgramSettings.DEFAULT_CRYPT_KEY   # Ensure crypt key is set to default
#user_password = db.GetSave(1)                                   # Get users saved password from db
#user_password = encryption.Decrypt(user_password)               # Decrypt saved password

toolHelper = ToolHelper(db, encryption)

gui = GUI(db, encryption, toolHelper)

# Check if entered password (gui) equals user_password
#if entered_password == user_password:
#    ProgramSettings.CRYPT_KEY = user_password                   # Set crypt key to user_password to use users password as encryption for the values:
#    print("Matches ->", entered_password, "<->", user_password)
#else:
#    print("Does not match")



### TESTING ###
# Create value
#someValue = Value(0, "Test", encryption.Encrypt("Something"))

# Add value to database and check result, override id
#result = db.CreateValue(someValue)
#if result > 0:
#    someValue.id = result

# Testing case "User sets new password"
#helper = ToolHelper(db, encryption)
#helper.UpdateUserPassword("test-password")