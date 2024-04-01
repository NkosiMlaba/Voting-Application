import os
import base64
from cryptography.fernet import Fernet

# Declaration section
current_directory = os.getcwd()
subdirectory_path = os.path.join(current_directory, "authentication")
key_path = os.path.join(subdirectory_path, 'key.txt')


def generate_key():
    return Fernet.generate_key()


def write_key(key):
    print(key)
    encoded_key = base64.urlsafe_b64encode(key).decode()
    with open(key_path, 'w') as file:
        file.write(encoded_key)


def read_key():
    with open(key_path, "r") as file:
        key  = file.read()
    key = base64.urlsafe_b64decode(key.encode())
    return key


def encrypt_email(email):
    key = read_key()
    
    cipher = Fernet(key)
    encrypted_email = cipher.encrypt(email.encode())
    return encrypted_email


def decrypt_email(encrypted_email):
    key = read_key()
    cipher = Fernet(key)
    decrypted_email = cipher.decrypt(encrypted_email).decode()
    return decrypted_email



