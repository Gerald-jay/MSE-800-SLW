# admin_service/booking_service.py
# -*- coding: utf-8 -*-
"""
Service layer for bookings (strict validation & conflict check)
"""

from datetime import datetime
from typing import List
from db.db_manager import DatabaseManager
from db.models import (
    Booking, Car, User,
    BOOKING_CONFIRMED
)
from common.validators import Validator
from common.exceptions import (
    ValidationError, NotFoundError, ConflictError, DatabaseError
)

DATE_FMT = "%d-%m-%Y"  # dd-mm-yyyy


class BookingService:
    """Booking service"""

    def __init__(self) -> None:
        # 幂等建表 / create table if not exists
        db = DatabaseManager().db
        db.create_tables([Booking])

    # ---------- helpers ----------
    @staticmethod
    def _parse_date(s: str):
        try:
            return datetime.strptime(s, DATE_FMT).date()
        except ValueError as e:
            raise ValidationError(f"Invalid date format {DATE_FMT}") from e

    # ---------- APIs ----------
    def create_booking(self, *, car_id: int, user_id: int,
                       start_date_str: str, end_date_str: str) -> Booking:
        """
        Create a booking
        Rules:
        - end ≥ start
        - Rental days must be between {min_days} and {max_days}
        - No overlap with confirmed bookings
        """
        # parse dates + basic validation
        start_date = self._parse_date(start_date_str)
        end_date = self._parse_date(end_date_str)
        if end_date < start_date:
            raise ValidationError("End date cannot be earlier than start date")

        # Check existence of car and user
        car = Car.get_or_none(Car.id == car_id)
        if not car:
            raise NotFoundError(f"Car not found: id={car_id}")
        user = User.get_or_none(User.id == user_id)
        if not user:
            raise NotFoundError(f"User not found: id={user_id}")

        # Rental days (inclusive)
        days = (end_date - start_date).days + 1
        # Car's own config validity (fallback)
        Validator.validate_days(car.min_days, car.max_days)
        if not (car.min_days <= days <= car.max_days):
            raise ValidationError(
                f"Rental days must be between {car.min_days} and {car.max_days}"
            )

        # Conflict check: interval [S, E] overlaps with existing confirmed booking
        # (start1 <= end2) and (end1 >= start2) means overlap between [start1, end1] and [start2, end2]
        conflict_exists = Booking.select().where(
            (Booking.car == car) &
            (Booking.status == BOOKING_CONFIRMED) &
            (Booking.start_date <= end_date) &
            (Booking.end_date >= start_date)
        ).exists()
        if conflict_exists:
            raise ConflictError("The car is already booked for this period")

        # create
        try:
            booking = Booking.create(
                car=car,
                user=user,
                start_date=start_date,
                end_date=end_date
            )
            return booking
        except Exception as e:
            raise DatabaseError(f"Create booking failed: {e}") from e

    def list_bookings(self) -> List[Booking]:
        """latest first"""
        return list(Booking.select().order_by(Booking.id.desc()))

    def cancel_booking(self, booking_id: int) -> Booking:
        """Only confirmed bookings can be cancelled"""
        booking = Booking.get_or_none(Booking.id == booking_id)
        if not booking:
            raise NotFoundError(f"Booking not found: id={booking_id}")
        if booking.status != BOOKING_CONFIRMED:
            raise ConflictError("Only confirmed bookings can be cancelled")
        try:
            booking.status = "cancelled"
            booking.save()
            return booking
        except Exception as e:
            raise DatabaseError(f"Cancel booking failed: {e}") from e
