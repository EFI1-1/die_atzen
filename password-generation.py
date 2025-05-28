import string
import secrets

def generate_password(length=12):
    characters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(secrets.choice(characters) for _ in range(length))

#Testaufruf
password = generate_password()
print(password)