import string
import secrets
class PasswordGeneration:
    """
    A class used to generate secure random passwords.
    """
    @staticmethod
    def Generate(length):
        """
        Generate a secure random password containing letters, digits, and punctuation.
        Parameters:
        length (int): The desired length of the generated password.
        Returns:
        str: A randomly generated password string of the specified length.
        """
        # Define the character pool: uppercase, lowercase letters, digits and punctuation
        characters = string.ascii_letters + string.digits + string.punctuation
        
        # Use secrets.choice for cryptographically secure random selection
        password = ''.join(secrets.choice(characters) for _ in range(length))
        
        return password