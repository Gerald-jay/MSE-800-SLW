"""
validators.py
Input validation module
"""
from datetime import date
from db.models import STATUS_CHOICES
from common.exceptions import ValidationError

class Validator:
    # Input validation utility

    @staticmethod
    def validate_username(name: str) -> bool:
        # username max length 20
        if not name or len(name) > 20:
            raise ValueError("Username must be ≤ 20 characters")
        return True

    @staticmethod
    def validate_email(email: str) -> bool:
        # email must be ≤ 60 chars and contain '@'
        if not email or len(email) > 60 or "@" not in email:
            raise ValueError("Invalid email or length > 60")
        return True
    
    @staticmethod
    def validate_password(password: str) -> bool:
        if not password or len(password) < 6:
            raise ValueError("Password must be ≥ 6 characters")
        elif len(password) > 30:
            raise ValueError("Password must be ≤ 30 characters")
        return True

    @staticmethod
    def validate_required(value: str, field: str):
        # Required field
        if not value or not value.strip():
            raise ValueError(f"{field} is required")
        return True

    @staticmethod
    def validate_str_len(value: str, max_len: int, field: str):
        """non-empty string with max length"""
        if not value or not value.strip():
            raise ValueError(f"{field} is required")
        if len(value) > max_len:
            raise ValueError(f"{field} must be ≤ {max_len} chars")
        return True

    @staticmethod
    def validate_nonneg_int(value: int, field: str):
        if int(value) < 0:
            raise ValueError(f"{field} must be ≥ 0")
        return True

    @staticmethod
    def validate_nonneg_float(value: float, field: str):
        if float(value) < 0:
            raise ValueError(f"{field} must be ≥ 0")
        return True
    
    @staticmethod
    def validate_make(make: str):
        if not make or len(make) > 50:
            raise ValidationError("Make is required and ≤ 50")
        return True

    @staticmethod
    def validate_model(model: str):
        if not model or len(model) > 50:
            raise ValidationError("Model is required and ≤ 50")
        return True

    @staticmethod
    def validate_year(year: int):
        this_year = date.today().year
        if not year or not (1980 <= year <= this_year + 1):
            raise ValidationError(f"Year must be between 1980 and {this_year+1}")
        return True

    @staticmethod
    def validate_kilometre(km: int):
        if not km or km < 0:
            raise ValidationError("Kilometre cannot be negative")
        return True

    @staticmethod
    def validate_daily_rate(rate: float):
        if rate < 0:
            raise ValidationError("Daily rate cannot be negative")
        return True

    @staticmethod
    def validate_days(min_days: int, max_days: int):
        if not min_days or min_days <= 0:
            raise ValidationError("Min days must be ≥ 1")
        if not max_days or max_days < min_days:
            raise ValidationError("Max days must be ≥ Min days")
        return True

    @staticmethod
    def validate_status(status: str):
        if status not in STATUS_CHOICES:
            choices = "/".join(STATUS_CHOICES)
            raise ValidationError(f"Status must be one of {choices}")
        return True
    
    @staticmethod
    def validate_name(s: str, label="Name", max_len=50):
        if not s or len(s) > max_len:
            raise ValidationError(f"{label} is required and ≤ {max_len} chars")
        return True

    @staticmethod
    def validate_phone(s: str, label="Phone", max_len=30):
        if not s or len(s) > max_len:
            raise ValidationError(f"{label} is required and ≤ {max_len} chars")
        return True

    @staticmethod
    def validate_id_document(s: str, label="ID Document", max_len=100):
        if not s or len(s) > max_len:
            raise ValidationError(f"{label} is required and ≤ {max_len} chars")
        return True

    @staticmethod
    def validate_amount(value: float):
        #  Can discounts/surcharges be negative? Usually not allowed
        #  Here require >= 0
        if value < 0:
            raise ValidationError("Amount cannot be negative")
        return True

    @staticmethod
    def validate_amount_type(t: str):
        from db.models import AMOUNT_TYPES
        if t not in AMOUNT_TYPES:
            raise ValidationError("invalid amount_type")
        return True

    @staticmethod
    def validate_rule_type(t: str):
        from db.models import PRULE_TYPES
        if t not in PRULE_TYPES:
            raise ValidationError("invalid rule_type")
        return True