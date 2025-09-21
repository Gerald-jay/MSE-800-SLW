# controllers/admin_audit_cli.py
# -*- coding: utf-8 -*-
from admin_service.audit_service import AuditService
from datetime import datetime

class AdminAuditCLI:
    def __init__(self, svc: AuditService):
        self.svc = svc

    def show(self):
        logs = self.svc.list_logs(limit=100)
        if not logs:
            print("No audit logs")
            return
        for l in logs:
            created: datetime = l.created_at # type: ignore
            print(f"#{l.id} {created.strftime('%d-%m-%Y %H:%M:%S')} user#{l.actor_user_id} {l.action} {l.target_type}({l.target_id}) | {l.detail or ''}")
