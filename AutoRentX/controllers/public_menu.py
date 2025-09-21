# controllers/public_menu.py
# -*- coding: utf-8 -*-
from getpass import getpass
from .base_menu import BaseMenu

class PublicMenu(BaseMenu):
    """Public (not logged-in) menu"""

    def show(self):
        while True:
            self.header("Car Rental CLI (Not logged in)")
            print("1) Login")
            print("2) Register")
            print("0) Exit")
            choice = input("Choose: ").strip()
            if choice == "1":
                email = input("Email: ").lower().strip()
                password = getpass("Password: ")
                user = self.auth.login(email, password)
                if user:
                    #  On successful login, return to main to switch to role menu
                    return user
            elif choice == "2":
                name = input("Name: ")
                email = input("Email: ").lower()
                password = getpass("Password: ")
                role = input("Role [customer/admin] (default customer): ").strip().lower() or "customer"
                self.auth.register(name, email, password, role)
            elif choice == "0":
                self.goodbye_and_exit()

            else:
                print("Invalid choice")
