# main.py
# -*- coding: utf-8 -*-
from typing import Optional
from auth_service import PeeweeAuthService
from db.models import User as DbUser
from admin_service.car_service import PeeweeCarService
from controllers import MenuFactory

class CarRentalCLIApp:
    def __init__(self):
        self.auth = PeeweeAuthService()
        self.cars = PeeweeCarService()
        self.current_user: Optional[DbUser] = None

    def run(self):
        while True:
            role = str(self.current_user.role) if self.current_user and self.current_user.role else None
            menu = MenuFactory.create(role, self.auth, self.cars, self.current_user)

            # PublicMenu.show() returns user on successful login; Admin/Customer returns None on logout
            user_or_none = menu.show()
            self.current_user = user_or_none  # User on login; None on logout

if __name__ == "__main__":
    CarRentalCLIApp().run()
