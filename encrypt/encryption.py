import os
import base64
from cryptography.fernet import Fernet
from dotenv import load_dotenv

load_dotenv()

def read_key_from_env():
    encoded_key = os.getenv("ENCRYPTION_KEY")
    if encoded_key is None:
        raise ValueError("Encryption key not found in the environment variables.")

    key = base64.urlsafe_b64decode(encoded_key.encode())
    return key


def generate_key():
    return Fernet.generate_key()


def write_key_to_env(key):
    encoded_key = base64.urlsafe_b64encode(key).decode()
    print(f"Add this to your .env file as ENCRYPTION_KEY={encoded_key}")


def encrypt_email(email):
    key = read_key_from_env()
    cipher = Fernet(key)
    encrypted_email = cipher.encrypt(email.encode())
    return encrypted_email


def decrypt_email(encrypted_email):
    key = read_key_from_env()
    cipher = Fernet(key)
    decrypted_email = cipher.decrypt(encrypted_email).decode()
    return decrypted_email

write_key_to_env(generate_key())