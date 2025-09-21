#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
auth_service.py
Peewee ORM + OOP
Authentication service (Peewee ORM + OOP)
"""
from attr import validate
from peewee import DoesNotExist
import hashlib, hmac, secrets
from typing import Optional
from abc import ABC, abstractmethod
from db.models import User, db
from common.validators import Validator

# ========== Password Utils ==========
def hash_password(password: str, salt: Optional[bytes] = None, iterations: int = 120_000):
    if salt is None:
        salt = secrets.token_bytes(16)
    digest = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, dklen=32)
    return salt, digest, iterations

def verify_password(password: str, salt: bytes, digest: bytes, iterations: int) -> bool:
    test = hashlib.pbkdf2_hmac("sha256", password.encode("utf-8"), salt, iterations, dklen=32)
    return hmac.compare_digest(test, digest)

# ========== Abstract Service ==========
class AuthService(ABC):
    """Authentication Service Interface"""

    @abstractmethod
    def register(self, name: str, email: str, password: str, role: str = "customer") -> bool:
        pass

    @abstractmethod
    def login(self, email: str, password: str):
        pass

# ========== Implementation ==========
class PeeweeAuthService(AuthService):
    """Authentication service implemented with Peewee"""

    def __init__(self):
        db.create_tables([User])  # Ensure tables exist

    def register(self, name: str, email: str, password: str, role: str = "customer") -> bool:
        try:
            # ====== Input validation ======
            Validator.validate_required(name, "Username")
            Validator.validate_required(email, "Email")
            Validator.validate_required(password, "Password")
            Validator.validate_username(name)
            Validator.validate_email(email)
            Validator.validate_password(password)
            if role not in ("customer", "admin"):
                raise ValueError("Role must be 'customer' or 'admin'")

            # ====== Password hashing ======
            salt, digest, iterations = hash_password(password)

            # ====== Write to database ======
            User.create(
                role=role, name=name, email=email,
                password_salt=salt, password_hash=digest,
                iterations=iterations
            )
            print(f"✓ Registered: {email} ({role})")
            return True
        except ValueError as ve:
            print(f"✗ Validation error: {ve}")
            return False
        except Exception as e:
            print(f"✗ Registration failed: {e}")
            return False

    def login(self, email: str, password: str):
        try:
            user = User.get(User.email == email)
            if not user.is_active:
                print("✗ Account disabled")
                return None
            if verify_password(password, user.password_salt, user.password_hash, user.iterations):
                print(f"✓ Login successful: {user.name} ({user.role})")
                return user
            else:
                print("✗ Wrong password")
                return None
        except DoesNotExist:
            print("✗ User not found")
            return None
