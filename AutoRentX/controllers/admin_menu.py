# controllers/admin_menu.py
# -*- coding: utf-8 -*-

from typing import Optional
from controllers.admin_booking_review_cli import AdminBookingReviewCLI
from db.models import User as DbUser
from common.typing_utils import safe_pk
from .base_menu import BaseMenu
from .car_admin_cli import CarAdminCLI

from controllers.admin_pricing_cli import AdminPricingCLI
from controllers.admin_audit_cli import AdminAuditCLI
from admin_service.pricing_service import PricingService
from admin_service.audit_service import AuditService
from admin_service.booking_review_service import BookingReviewService

class AdminMenu(BaseMenu):
    """Admin menu"""
    def __init__(self, auth, cars, current_user: Optional[DbUser] = None):
        super().__init__(auth, cars, current_user)
        self.audit = AuditService()
        self.pricing = PricingService(self.audit)
        self.pricing_cli = AdminPricingCLI(self.pricing, safe_pk(self.current_user))
        self.audit_cli = AdminAuditCLI(self.audit)
        self.booking_review = AdminBookingReviewCLI(BookingReviewService(self.audit),
                                                    safe_pk(self.current_user))

    def show(self):
        # Logged-in state is ensured in main, directly show admin main menu here
        while True:
            if self.current_user:
                self.header(f"Car Rental CLI (Admin: {self.current_user.name})")
            else:
                self.header("Car Rental CLI (Admin: Not logged in)")
            print("1) Who am I")
            print("2) Car management")
            print("3) Booking review")
            print("4) Pricing rules")
            print("5) Audit logs")
            print("9) Logout")
            print("0) Exit")
            choice = input("Choose: ").strip()

            if choice == "1":
                u = self.current_user
                if u:
                    print(f"{u.name} <{u.email}> ({u.role})")
                else:
                    print("No user currently logged in")

            elif choice == "2":
                CarAdminCLI(self.cars, safe_pk(self.current_user), self.audit).show()
            elif choice == "3":
                self.booking_review.uid = safe_pk(self.current_user)
                self.booking_review.show()
            elif choice == "4":
                self.pricing_cli.uid = safe_pk(self.current_user)  # ensure actor id
                self.pricing_cli.show()
            elif choice == "5":
                self.audit_cli.show()
            elif choice == "9":
                # Hand over to main, set to not logged in
                return None

            elif choice == "0":
                self.goodbye_and_exit()
            else:
                print("Invalid choice")

