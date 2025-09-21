# customer_service/profile_service.py
# -*- coding: utf-8 -*-
from typing import Optional
from datetime import datetime
from db.db_manager import DatabaseManager
from db.models import CustomerProfile
from db.models import User as DbUser
from common.validators import Validator
from common.exceptions import NotFoundError, DatabaseError
from admin_service.audit_service import AuditService

class ProfileService:
    def __init__(self, audit: Optional[AuditService] = None):
        db = DatabaseManager().db
        db.create_tables([CustomerProfile])
        self.audit = audit or AuditService()

    def get_my_profile(self, user_id: int) -> Optional[CustomerProfile]:
        return CustomerProfile.get_or_none(CustomerProfile.user == user_id)

    def create_or_update(self, *, actor_user_id: int, user_id: int, first_name: str, last_name: str, phone: str, id_document: str) -> CustomerProfile:
        # validate
        Validator.validate_name(first_name, "First name")
        Validator.validate_name(last_name, "Last name")
        Validator.validate_phone(phone)
        Validator.validate_id_document(id_document)

        user = DbUser.get_or_none(DbUser.id == user_id)
        if not user:
            raise NotFoundError("User not found")

        try:
            prof = CustomerProfile.get_or_none(CustomerProfile.user == user_id)
            if prof:
                prof.first_name = first_name.strip()
                prof.last_name = last_name.strip()
                prof.phone = phone.strip()
                prof.id_document = id_document.strip()
                prof.updated_at = datetime.now()
                prof.save()
                self.audit.write(actor_user_id=actor_user_id, action="update_profile", target_type="profile", target_id=prof.id)
                return prof
            else:
                prof = CustomerProfile.create(
                    user=user,
                    first_name=first_name.strip(),
                    last_name=last_name.strip(),
                    phone=phone.strip(),
                    id_document=id_document.strip()
                )
                self.audit.write(actor_user_id=actor_user_id, action="create_profile", target_type="profile", target_id=prof.id)
                return prof
        except Exception as e:
            raise DatabaseError(f"Failed to save profile: {e}") from e
