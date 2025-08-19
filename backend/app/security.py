import hashlib
from typing import Optional
from passlib.hash import bcrypt
from cryptography.fernet import Fernet, InvalidToken

def hash_password(plain: str) -> str:
    return bcrypt.using(rounds=12).hash(plain)

def verify_password(plain: str, hashed: str) -> bool:
    try:
        return bcrypt.verify(plain, hashed)
    except Exception:
        return False

def email_fingerprint(email: str) -> str:
    canon = email.strip().lower().encode("utf-8")
    return hashlib.sha256(canon).hexdigest()

def encrypt_email(email: str, key: str) -> bytes:
    f = Fernet(key.encode() if isinstance(key, str) else key)
    return f.encrypt(email.encode("utf-8"))

def decrypt_email(token: bytes, key: str) -> Optional[str]:
    try:
        f = Fernet(key.encode() if isinstance(key, str) else key)
        return f.decrypt(token).decode("utf-8")
    except (InvalidToken, Exception):
        return None
