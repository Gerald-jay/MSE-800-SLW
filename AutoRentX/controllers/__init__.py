# controllers/__init__.py
# -*- coding: utf-8 -*-
from typing import Optional
from auth_service import PeeweeAuthService
from db.models import User as DbUser
from admin_service.car_service import PeeweeCarService
from .public_menu import PublicMenu
from .admin_menu import AdminMenu
from .customer_menu import CustomerMenu

class MenuFactory:
    """Factory Method for Menus"""

    @staticmethod
    def create(role: Optional[str],
               auth: PeeweeAuthService,
               cars: PeeweeCarService,
               current_user: Optional[DbUser] = None):
        if role is None:
            return PublicMenu(auth, cars, current_user)
        if role == "admin":
            return AdminMenu(auth, cars, current_user)
        return CustomerMenu(auth, cars, current_user)
