# admin_service/booking_review_service.py
# -*- coding: utf-8 -*-
from typing import Any, List, Optional

from pyparsing import cast
from db.db_manager import DatabaseManager
from db.models import Booking, Car, BOOKING_PENDING, BOOKING_CONFIRMED, BOOKING_CANCELLED, STATUS_AVAILABLE, STATUS_RESERVED
from admin_service.audit_service import AuditService
from common.exceptions import NotFoundError, ConflictError

class BookingReviewService:
    def __init__(self, audit: Optional[AuditService] = None):
        DatabaseManager().db.create_tables([Booking])
        self.audit = audit or AuditService()

    def list_pending(self) -> List[Booking]:
        return list(Booking.select(Booking).where(Booking.status == BOOKING_PENDING).order_by(Booking.id.desc()))

    def _recompute_car_status(self, car: Car) -> None:
        active_exists = (Booking
            .select()
            .where((Booking.car == car) &
                   (Booking.status.in_([BOOKING_PENDING, BOOKING_CONFIRMED])))
            .exists())
        cast(Any, car).status = STATUS_RESERVED if active_exists else STATUS_AVAILABLE
        car.save()

    def approve(self, *, actor_user_id: int, booking_id: int) -> Booking:
        b = Booking.get_or_none(Booking.id == booking_id)
        if not b: raise NotFoundError("Not found")
        if b.status != BOOKING_PENDING: raise ConflictError("Invalid status")
        b.status = BOOKING_CONFIRMED
        b.save()
        self._recompute_car_status(b.car)
        self.audit.write(actor_user_id=actor_user_id, action="approve_booking",
                         target_type="booking", target_id=b.id, detail=f"car#{b.car.id}")
        return b

    def reject(self, *, actor_user_id: int, booking_id: int) -> Booking:
        b = Booking.get_or_none(Booking.id == booking_id)
        if not b: raise NotFoundError("Not found")
        if b.status != BOOKING_PENDING: raise ConflictError("Invalid status")
        b.status = BOOKING_CANCELLED
        b.save()
        self._recompute_car_status(b.car)
        self.audit.write(actor_user_id=actor_user_id, action="reject_booking",
                         target_type="booking", target_id=b.id, detail=f"car#{b.car.id}")
        return b
