# controllers/car_admin_cli.py
# -*- coding: utf-8 -*-
"""
Admin car-management menu (CLI controller)
"""

from common.exceptions import AppError, NotFoundError, ValidationError, ConflictError, DatabaseError
from admin_service.car_service import PeeweeCarService
from admin_service.audit_service import AuditService
from common.input_utils import prompt_int, prompt_float, prompt_str, prompt_choice, prompt_id

class CarAdminCLI:
    """Admin car-management CLI"""

    def __init__(self, car_service: PeeweeCarService, current_user_id: int, audit: AuditService | None = None):
        self.cars = car_service
        self.uid = current_user_id
        self.audit = audit or AuditService()

    def show(self):
        """loop menu"""
        while True:
            print("""
=== Car Management ===
1) Add car
2) Update car
3) List cars
4) Update car status
0) Back
""")
            choice = input("Choose: ").strip()

            if choice == "1":
                self._add_car()
            elif choice == "2":
                self._update_car()
            elif choice == "3":
                self._list_cars()
            elif choice == "4":
                self._update_status()
            elif choice == "0":
                break
            else:
                print("Invalid choice")

    # ---------- actions ----------
    def _add_car(self):
        make = prompt_str("Make")                                
        model = prompt_str("Model")                              
        year = prompt_int("Year")                               
        kilometre = prompt_int("Kilometre (km)")                 
        daily_rate = prompt_float("Daily rate")                  

        # Days: friendly validation "min ≤ max" at the interaction layer
        while True:
            min_days = prompt_int("Min days")
            max_days = prompt_int("Max days")
            if max_days >= min_days:
                break
            print("✗ Max days must be ≥ Min days")

        status = prompt_choice(
            "Status", ["available", "unavailable", "maintenance"], "available"
        )

        # Service layer does strict validation (double check) and raise custom exceptions
        try:
            car = self.cars.create_car(
                make=make, model=model, year=year, kilometre=kilometre,
                daily_rate=daily_rate, min_days=min_days, max_days=max_days, status=status
            )
            print(f"✓ Created: #{car.id} {car.make} {car.model}")
        except ValidationError as ve:
            print("✗ Validation error:", ve)
        except ConflictError as ce:
            print("✗ Conflict:", ce)
        except DatabaseError as de:
            print("✗ Database error:", de)
        except AppError as ae:
            print("✗ Application error:", ae)
        except Exception as e:
            print("✗ Unknown error:", e)

    def _update_car(self):
        car_id = prompt_id("Car ID to update")
        if car_id is None:
            return

        car = self.cars.get_car(car_id)
        if not car:
            print(f"✗ Car ID {car_id} not found")
            return

        # press Enter to keep, or type to overwrite
        make       = prompt_str("Make", car.make)
        model      = prompt_str("Model", car.model)
        year       = prompt_int("Year", car.year)
        kilometre  = prompt_int("Kilometre (km)", car.kilometre)
        daily_rate = prompt_float("Daily rate", car.daily_rate)
        status     = prompt_choice("Status", ["available","unavailable","maintenance"], car.status)

        try:
            updated = self.cars.update_car(
                car_id, actor_user_id=self.uid,
                make=make, model=model, year=year, kilometre=kilometre,
                daily_rate=daily_rate, status=status
            )
            print(f"✓ Updated: #{updated.id} {updated.make} {updated.model}")
        except ValidationError as ve:
            print("✗ Validation error:", ve)
        except NotFoundError as ne:
            print("✗ Not found:", ne)
        except ConflictError as ce:
            print("✗ Conflict:", ce)
        except DatabaseError as de:
            print("✗ Database error:", de)
        except AppError as ae:
            print("✗ Application error:", ae)
        except Exception as e:
            print("✗ Unknown error:", e)

    def _list_cars(self):
        cars = self.cars.list_cars()
        if not cars:
            print(" No cars")
            return
        for c in cars:
            print(f"#{c.id} {c.make} {c.model} {c.year} | {c.kilometre} km | "
                  f"${c.daily_rate}/day | {c.status}")

    def _update_status(self):
        car_id = prompt_id("Car ID")
        if car_id is None: return
        st = prompt_choice("Status", ["available","reserved","unavailable","maintenance"], "available")
        try:
            self.cars.update_car(car_id, actor_user_id=self.uid, status=st)   # 只传 status / pass status only
            print("✓ Status updated")
        except Exception as e:
            print("✗ Error:", e)