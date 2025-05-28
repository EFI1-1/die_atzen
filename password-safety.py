import re  # Import regular expressions module

def password_check(password: str) -> bool:
    """Checks if a password is considered strong."""
    
    # Check minimum length
    if len(password) < 8:
        print("Passwort zu kurz (mind. 8 Zeichen).")  # Password too short
        return False

    # Check for at least one uppercase letter
    if not re.search(r"[A-Z]", password):
        print("Mindestens ein Großbuchstabe fehlt.")  # Missing uppercase letter
        return False

    # Check for at least one lowercase letter
    if not re.search(r"[a-z]", password):
        print("Mindestens ein Kleinbuchstabe fehlt.")  # Missing lowercase letter
        return False

    # Check for at least one digit
    if not re.search(r"[0-9]", password):
        print("Mindestens eine Zahl fehlt.")  # Missing digit
        return False

    # Check for at least one special character
    if not re.search(r"[!@#$%^&*()_+\-=\[\]{};:'\"\\|,.<>/?]", password):
        print("Mindestens ein Sonderzeichen fehlt.")  # Missing special character
        return False

    # If all checks pass
    print("Passwort ist stark.")  # Password is strong
    return True

if __name__ == "__main__":
    pw = input("Gib ein Passwort ein: ")  # Prompt user for password
    password_check(pw)