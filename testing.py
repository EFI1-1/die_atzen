# Create value
#someValue = Value(0, "Test",  encryption.Encrypt("Something"))

# Add value to database and check result, override id
#result = db.CreateValue(someValue)
#if result > 0:
#    someValue.id = result

# Change and save value
#someValue.name = "A changed name"
#someValue.key = encryption.Encrypt("A changed key")
#if not db.SaveValue(someValue):
#    print("An error occured saving the value in the database")

# Give out all values in db
#values = db.GetAllValues()
#for v in values:
#    print(f"ID: {v.id}, Name: {v.name}, Key: {v.key}")

# Delete value
#if db.DeleteValue(someValue):
#    print("Value deleted")
#else:
#    print("An error occured deleting the value")