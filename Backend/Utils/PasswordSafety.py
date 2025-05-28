import re                       # Import the regular expressions module
from tkinter import messagebox  # Import messagebox for GUI notifications

class PasswordSafety:
    DEFAULT_INFO_HEAD = "Warnung"
    DEFAULT_INFO = "Dein Passwort ist nicht sicher genug!\n\n"

    def Check(self, password: str) -> bool:
        """
        Evaluates the strength of a given password based on common security criteria.
        Also prints a messagebox (tkinter)

        A strong password must meet all of the following requirements:
        - Minimum length of 8 characters
        - Contains at least one uppercase letter (A-Z)
        - Contains at least one lowercase letter (a-z)
        - Contains at least one digit (0-9)
        - Contains at least one special character (e.g., !, @, #, etc.)

        Parameters:
        password (str): The password string to be evaluated.

        Returns:
        bool: True if the password is strong, False otherwise.
        """
        
        # Check for minimum length
        if len(password) < 8:
            messagebox.showwarning(self.DEFAULT_INFO_HEAD, f"{self.DEFAULT_INFO} Passwort zu kurz (mind. 8 Zeichen).")
            return False

        # Check for at least one uppercase letter
        if not re.search(r"[A-Z]", password):
            messagebox.showwarning(self.DEFAULT_INFO_HEAD, f"{self.DEFAULT_INFO} Mindestens ein Großbuchstabe fehlt.")
            return False

        # Check for at least one lowercase letter
        if not re.search(r"[a-z]", password):
            messagebox.showwarning(self.DEFAULT_INFO_HEAD, f"{self.DEFAULT_INFO} Mindestens ein Kleinbuchstabe fehlt.")
            return False

        # Check for at least one digit
        if not re.search(r"[0-9]", password):
            messagebox.showwarning(self.DEFAULT_INFO_HEAD, f"{self.DEFAULT_INFO} Mindestens eine Zahl fehlt.")
            return False

        # Check for at least one special character
        if not re.search(r"[!@#$%^&*()_+\-=\[\]{};:'\"\\|,.<>/?]", password):
            messagebox.showwarning(self.DEFAULT_INFO_HEAD, f"{self.DEFAULT_INFO} Mindestens ein Sonderzeichen fehlt.")
            return False
        
        # All checks passed; password is strong
        return True