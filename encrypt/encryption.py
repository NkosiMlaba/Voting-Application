import os
import base64
from cryptography.fernet import Fernet
import sys

from dotenv import load_dotenv

load_dotenv()

def read_key_from_env():
    """
    Read the encryption key from the environment variables.

    The function retrieves the encryption key from the environment variable named "ENCRYPTION_KEY".
    If the key is not found, it raises a ValueError with an appropriate error message.

    Returns:
        bytes: The encryption key as bytes.
    """
    encoded_key = os.getenv("ENCRYPTION_KEY")
    if encoded_key is None:
        sys.exit("""ENCRYPTION_KEY not found in environment variables. \n        Please add it to your .env file.
                 \n        Example: \n            ENCRYPTION_KEY=your_encryption_key (see README.md for instructions)
                 \n\nExiting Application...""")

    key = base64.urlsafe_b64decode(encoded_key.encode())
    return key


def generate_key():
    """
    Generate a new encryption key using the Fernet algorithm.

    Returns:
        bytes: The newly generated encryption key as bytes.
    """
    return Fernet.generate_key()


def write_key_to_env(key):
    """
    The function encodes the provided encryption key using base64 and prints a message
    instructing the user to add the encoded key to their .env file.

    Args:
        key (bytes): The encryption key to be written to the environment variables.
    """
    encoded_key = base64.urlsafe_b64encode(key).decode()
    print(f"Add this to your .env file as ENCRYPTION_KEY={encoded_key}")


def encrypt_email(email):
    """
    Encrypt an email address using the encryption key.

    The function retrieves the encryption key from the environment variables, creates a Fernet
    cipher object, and then encrypts the provided email address.

    Args:
        email (str): The email address to be encrypted.

    Returns:
        bytes: The encrypted email address as bytes.
    """
    key = read_key_from_env()
    cipher = Fernet(key)
    encrypted_email = cipher.encrypt(email.encode())
    return encrypted_email


def decrypt_email(encrypted_email):
    """
    Decrypt an encrypted email address using the encryption key.

    The function retrieves the encryption key from the environment variables, creates a Fernet
    cipher object, and then decrypts the provided encrypted email address.

    Args:
        encrypted_email (bytes): The encrypted email address to be decrypted.

    Returns:
        str: The decrypted email address as a string.
    """
    key = read_key_from_env()
    cipher = Fernet(key)
    decrypted_email = cipher.decrypt(encrypted_email).decode()
    return decrypted_email

write_key_to_env(generate_key())