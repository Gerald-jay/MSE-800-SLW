# admin_service/car_service.py
# -*- coding: utf-8 -*-
"""
Car service (admin)
Strict validation + unified exceptions
"""
from turtle import st
from typing import Optional
from peewee import IntegrityError, DoesNotExist
from db.db_manager import DatabaseManager
from admin_service.audit_service import AuditService
from db.models import Car, Payment
from common.validators import Validator
from common.exceptions import NotFoundError, ConflictError, DatabaseError

class PeeweeCarService:
    """Car service"""
    def __init__(self, audit: AuditService | None = None):
        DatabaseManager().db.create_tables([Payment])
        self.audit = audit or AuditService()

    def create_car(self, *, make: str, model: str, year: int, kilometre: int,
                   daily_rate: float, min_days: int, max_days: int, status: str = "available") -> Car:
        # ---- business validation ----
        Validator.validate_make(make)
        Validator.validate_model(model)
        Validator.validate_year(year)
        Validator.validate_kilometre(kilometre)
        Validator.validate_daily_rate(daily_rate)
        Validator.validate_days(min_days, max_days)
        Validator.validate_status(status)

        try:
            car = Car.create(
                make=make.strip(),
                model=model.strip(),
                year=year,
                kilometre=kilometre,
                daily_rate=daily_rate,
                min_days=min_days,
                max_days=max_days,
                status=status,
            )
            # No print in service layer; return entity or ID
            return car
        except IntegrityError as ie:
            # e.g. if unique constraint (e.g. license plate) is added later, convert to ConflictError here
            raise ConflictError(f"Create car failed: {ie}") from ie
        except Exception as e:
            raise DatabaseError(f"Create car failed: {e}") from e

    def get_car(self, car_id: int) -> Optional[Car]:
        try:
            return Car.get(Car.id == car_id)
        except DoesNotExist:
            return None

    def list_cars(self) -> list[Car]:
        return list(Car.select().order_by(Car.id.desc()))

    def update_car(self, car_id: int,*, actor_user_id: int, **fields) -> Car:
        # get the object first
        car = self.get_car(car_id)
        if not car:
            raise NotFoundError(f"Car not found: id={car_id}")

        # extract & validate (only the fields passed in)
        if "make" in fields:
            Validator.validate_make(fields["make"])
            car.make = fields["make"].strip()
        if "model" in fields:
            Validator.validate_model(fields["model"])
            car.model = fields["model"].strip()
        if "year" in fields:
            Validator.validate_year(fields["year"])
            car.year = fields["year"]
        if "kilometre" in fields:
            Validator.validate_kilometre(fields["kilometre"])
            car.kilometre = fields["kilometre"]
        if "daily_rate" in fields:
            Validator.validate_daily_rate(fields["daily_rate"])
            car.daily_rate = fields["daily_rate"]
        if "status" in fields:
            Validator.validate_status(fields["status"])
            car.status = fields["status"]

        try:
            car.save()
            self.audit.write(actor_user_id=actor_user_id, action="update_car", target_type="car", target_id=car_id, detail=f"status={st}")
            return car
        except IntegrityError as ie:
            raise ConflictError(f"Update car failed: {ie}") from ie
        except Exception as e:
            raise DatabaseError(f"Update car failed: {e}") from e
