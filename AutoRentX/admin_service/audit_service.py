# admin_service/audit_service.py
# -*- coding: utf-8 -*-
from typing import Optional, List
from db.db_manager import DatabaseManager
from db.models import AuditLog

class AuditService:
    def __init__(self):
        db = DatabaseManager().db
        db.create_tables([AuditLog])

    def write(self, *, actor_user_id: int, action: str, target_type: str, target_id: Optional[int]=None, detail: Optional[str]=None) -> AuditLog:
        return AuditLog.create(
            actor_user_id=actor_user_id,
            action=action,
            target_type=target_type,
            target_id=target_id,
            detail=detail
        )

    def list_logs(self, limit: int = 100) -> List[AuditLog]:
        return list(AuditLog.select().order_by(AuditLog.id.desc()).limit(limit))
