from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import padding
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives import hashes
from base64 import b64encode, b64decode
import os

# Generate a 32-byte (256-bit) AES key from a password using PBKDF2
# We use a password instead of a randomly generated key so that the key can be consistently recreated when needed.
password = b"?l4![e_-_~:[C8oZO#Y3K,z53Mb$#2x6"

# Derive a secure key using PBKDF2 (Password-Based Key Derivation Function 2)
# This allows for secure transformation of a password into a fixed-length cryptographic key.
kdf = PBKDF2HMAC(
    algorithm=hashes.SHA256(),              # Secure hashing algorithm used in key derivation
    length=32,                              # Length of the AES key: 32 bytes = 256 bits
    salt=b"bd5kqV<5/|N?hyY!AK(9[:-eF.3h",   # Fixed 28-string-salt-value ensures the same key is derived each time for this password
    iterations=100000,                      # Number of iterations increases computation cost to resist brute-force attacks
    backend=default_backend()               # Default backend provides cryptographic primitives
)
key = kdf.derive(password)  # Derive the AES key from the password and salt using PBKDF2

# Encrypt function
def Encrypt(message: str) -> str:
    # Convert string to bytes, since encryption operates on bytes, not text
    data = message.encode('utf-8')

    # Pad the data to be a multiple of 16 bytes (AES block size is 128 bits or 16 bytes)
    padder = padding.PKCS7(128).padder()  # PKCS7 padding is standard for block ciphers
    padded_data = padder.update(data) + padder.finalize()  # Apply padding to the message

    # Generate a random 16-byte IV (Initialization Vector)
    # IV adds randomness to encryption to prevent repeated patterns
    iv = os.urandom(16)

    # Create AES cipher in CBC (Cipher Block Chaining) mode
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    encryptor = cipher.encryptor()

    # Encrypt the padded data
    ciphertext = encryptor.update(padded_data) + encryptor.finalize()

    # Return the IV + ciphertext, base64 encoded for transmission/storage as text
    return b64encode(iv + ciphertext).decode('utf-8')

# Decrypt function
def Decrypt(encryptedMessage: str) -> str:
    # Decode the base64-encoded input to raw bytes
    raw_data = b64decode(encryptedMessage)

    # Extract IV (first 16 bytes) and ciphertext (remaining bytes)
    iv = raw_data[:16]  # IV must be used exactly as it was during encryption
    ciphertext = raw_data[16:]  # The actual encrypted content

    # Create AES cipher in CBC mode using the same key and extracted IV
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
    decryptor = cipher.decryptor()

    # Decrypt the ciphertext and then remove the padding
    padded_plaintext = decryptor.update(ciphertext) + decryptor.finalize()
    unpadder = padding.PKCS7(128).unpadder()  # Remove the padding after decryption
    plaintext = unpadder.update(padded_plaintext) + unpadder.finalize()

    # Decode bytes back to UTF-8 string and return
    return plaintext.decode('utf-8')