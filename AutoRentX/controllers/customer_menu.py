# controllers/customer_menu.py
# -*- coding: utf-8 -*-
from typing import Optional
from common.typing_utils import safe_pk
from db.models import User as DbUser
from .base_menu import BaseMenu
from controllers.customer_profile_cli import CustomerProfileCLI
from controllers.customer_rent_cli import CustomerRentCLI
from customer_service.profile_service import ProfileService
from customer_service.rent_service import RentService

class CustomerMenu(BaseMenu):
    """Customer menu"""
    def __init__(self, auth, cars, current_user: Optional[DbUser] = None):
        super().__init__(auth, cars, current_user)
        uid: int = int(self.current_user.id) if self.current_user and isinstance(self.current_user.id, (int, str)) else 0
        self.profile_cli = CustomerProfileCLI(ProfileService(), uid)
        self.rent_cli = CustomerRentCLI(RentService(), ProfileService(), uid)

    def show(self):
        while True:
            if self.current_user:
                self.header(f"Car Rental CLI (Customer: {self.current_user.name})")
            else:
                self.header("Car Rental CLI (Customer: Not logged in)")
            print("1) My profile")
            print("2) Rent a car")
            print("9) Logout")
            print("0) Exit")
            choice = input("Choose: ").strip()
            if choice == "1":
                self.profile_cli.uid = safe_pk(self.current_user)
                self.profile_cli.show()
            elif choice == "2":
                self.rent_cli.uid = safe_pk(self.current_user)
                self.rent_cli.show()
            elif choice == "9":
                return None
            elif choice == "0":
                self.goodbye_and_exit()
            else:
                print("Invalid choice")
