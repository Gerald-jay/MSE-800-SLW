# common/exceptions.py
# -*- coding: utf-8 -*-
"""
Unified application exceptions
"""

class AppError(Exception):
    """Base application error"""
    pass

class ValidationError(AppError):
    """Business validation error"""
    pass

class NotFoundError(AppError):
    """Resource not found"""
    pass

class ConflictError(AppError):
    """Conflict (e.g., unique constraint)"""
    pass

class AppPermissionError(AppError):
    """Permission denied (avoid shadowing built-in)"""
    pass

class DatabaseError(AppError):
    """DB error wrapper"""
    pass
