import base64
import secrets

from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC

backend = default_backend()

def _derive_key(password: bytes, salt: bytes, iterations: int) -> bytes:
    """Derive a secret key from a given password and salt"""
    kdf = PBKDF2HMAC(
        algorithm=hashes.SHA256(), length=32, salt=salt,
        iterations=iterations, backend=backend)
    return base64.urlsafe_b64encode(kdf.derive(password))

def password_encrypt(password: bytes, key: str, iteration: int) -> bytes:
    salt = secrets.token_bytes(16)
    key = _derive_key(key.encode(), salt, iteration)
    return base64.urlsafe_b64encode(
        b'%b%b%b' % (
            salt,
            iteration.to_bytes(4, byteorder='big'),
            base64.urlsafe_b64decode(Fernet(key).encrypt(password)),
        )
    )

def password_decrypt(password: bytes, key: str) -> bytes:
    decoded = base64.urlsafe_b64decode(password)
    salt, iteration, password = decoded[:16], decoded[16:20], base64.urlsafe_b64encode(decoded[20:])
    iterations = int.from_bytes(iteration, 'big')
    key = _derive_key(key.encode(), salt, iterations)
    return Fernet(key).decrypt(password)
