# controllers/base_menu.py
# -*- coding: utf-8 -*-
from typing import Optional
from db.models import db
from auth_service import PeeweeAuthService
from db.models import User as DbUser
from admin_service.car_service import PeeweeCarService

class BaseMenu:
    """Base class for menus"""

    def __init__(self,
                 auth: PeeweeAuthService,
                 cars: PeeweeCarService,
                 current_user: Optional[DbUser] = None):
        self.auth = auth
        self.cars = cars
        self.current_user = current_user

    def set_current_user(self, user: Optional[DbUser]):
        self.current_user = user

    def header(self, title: str):
        print(f"\n=== {title} ===")

    def goodbye_and_exit(self):
        print("Goodbye")
        try:
            db.close()
        except Exception:
            pass
        raise SystemExit(0)
