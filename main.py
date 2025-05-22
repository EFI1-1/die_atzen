# Program initilization

from Backend.Utils.DBManager import DBManager
from Backend.Utils.Encryption import Encryption
from Backend.Value import Value
from Backend.ProgramSettings import ProgramSettings

### Testing ###

entered_password = ""

# Create database
db = DBManager()

# Update settings
# Get users saved password from db
user_enc_password = db.GetSave(1)
print(user_enc_password)
# decrypt saved password and use default encryption value
#ProgramSettings.CRYPTKEY = ProgramSettings.DEFAULT_CRYPT_KEY
#user_enc_password = Encryption.Decrypt(user_enc_password)
# check entered password with user_enc_password
#if entered_password == user_enc_password:
    # Set crypt key to user_enc_password:
#    ProgramSettings.CRYPT_KEY = user_enc_password
#else:
#    print("Does not match")

# Create value
someValue = Value(0, "Test", "Something")

# Add value to database and check result, override id
result = db.CreateValue(someValue)
if result > 0:
    someValue.id = result

# Change and save value
someValue.name = "A changed name"
someValue.key = "A changed key"
if not db.SaveValue(someValue):
    print("An error occured saving the value in the database")

# Give out all values in db
values = db.GetAllValues()
for v in values:
    print(f"ID: {v.id}, Name: {v.name}, Key: {v.key}")

# Delete value
if db.DeleteValue(someValue):
    print("Value deleted")
else:
    print("An error occured deleting the value")