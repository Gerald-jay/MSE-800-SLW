# customer_service/rent_service.py
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Tuple
from common.payment_app import PaymentGateway, PaymentRequest
from db.models import STATUS_RESERVED, Car, Booking, CustomerProfile, BOOKING_CONFIRMED, BOOKING_PENDING, STATUS_AVAILABLE, Payment
from db.db_manager import DatabaseManager
from admin_service.pricing_service import PricingService, DATE_FMT
from admin_service.audit_service import AuditService
from common.exceptions import ValidationError, NotFoundError, ConflictError, DatabaseError

class RentService:
    def __init__(self, pricing: PricingService | None = None, audit: AuditService | None = None):
        db = DatabaseManager().db
        db.create_tables([Booking])  # idempotent
        self.pricing = pricing or PricingService()
        self.audit = audit or AuditService()

    @staticmethod
    def _parse_date(s: str):
        try:
            return datetime.strptime(s, DATE_FMT).date()
        except ValueError as e:
            raise ValidationError(f"Invalid date format {DATE_FMT}") from e

    def available_cars(self, start_str: str, end_str: str) -> List[Car]:
        start = self._parse_date(start_str)
        end = self._parse_date(end_str)
        if end < start:
            raise ValidationError("End date cannot be earlier than start date")

        # only return cars with status=available and no confirmed bookings in the period
        # from db.models import Booking
        overlapping = (Booking
                       .select(Booking.car)
                       .where((Booking.status == BOOKING_CONFIRMED) &
                              (Booking.start_date <= end) &
                              (Booking.end_date >= start)))
        q = Car.select().where((Car.status == STATUS_AVAILABLE) & (Car.id.not_in(overlapping)))
        return list(q.order_by(Car.id.desc()))

    def list_my_bookings(self, user_id: int) -> list[Booking]:
        """My bookings"""
        return list(Booking
            .select(Booking)
            .where((Booking.user == user_id) &
                   (Booking.status.in_([BOOKING_PENDING, BOOKING_CONFIRMED])))
            .order_by(Booking.id.desc()))

    def quote(self, car_id: int, start_str: str, end_str: str) -> Tuple[int, float, list[tuple[int, float]], float, float]:
        start = self._parse_date(start_str)
        end = self._parse_date(end_str)
        car = Car.get_or_none(Car.id == car_id)
        if not car or car.status != STATUS_AVAILABLE:
            raise NotFoundError("Car not found or not available")

        days = (end - start).days + 1
        base_cost, adjustments, grand_total, daily_rate = self.pricing.quote(car=car, start_date=start, end_date=end)
        return days, base_cost, adjustments, grand_total, daily_rate

    def create_pending_booking(self, *, actor_user_id: int, user_id: int, car_id: int, start_str: str, end_str: str) -> Booking:
        start = self._parse_date(start_str)
        end = self._parse_date(end_str)
        if end < start:
            raise ValidationError("End date cannot be earlier than start date")

        car = Car.get_or_none(Car.id == car_id)
        if not car:
            raise NotFoundError("Car not found")
        prof = CustomerProfile.get_or_none(CustomerProfile.user == user_id)

        if not prof:
            raise ConflictError("Incomplete personal information, unable to place order")

        # Check availability (no conflict with confirmed bookings)
        conflict = Booking.select().where(
            (Booking.car == car) &
            (Booking.status == BOOKING_CONFIRMED) &
            (Booking.start_date <= end) &
            (Booking.end_date >= start)
        ).exists()
        if conflict:
            raise ConflictError("The car is already booked for this period")

        # Quote
        days, base_cost, adjustments, grand_total, daily_rate = self.quote(car_id, start_str, end_str)

        try:
            b = Booking.create(
                car=car,
                user=user_id,
                start_date=start,
                end_date=end,
                status=BOOKING_PENDING,  # pending
                days=days,
                base_daily_rate=car.daily_rate,
                base_cost=base_cost,
                adj_total=sum(d for _, d in adjustments),
                grand_total=grand_total,
                snap_first_name=prof.first_name,
                snap_last_name=prof.last_name,
                snap_phone=prof.phone,
                snap_id_document=prof.id_document
            )
            self.audit.write(actor_user_id=actor_user_id, action="create_booking", target_type="booking", target_id=b.id,
                             detail=f"car={car_id} {start_str}->{end_str} pending")
            return b
        except Exception as e:
            raise DatabaseError(f"Failed to create booking: {e}") from e

    def _recompute_car_status(self, car: Car) -> None:
        """Occupy or free car by active bookings"""
        active_exists = (Booking
            .select()
            .where((Booking.car == car) &
                   (Booking.status.in_([BOOKING_PENDING, BOOKING_CONFIRMED])))
            .exists())
        status_value: str = STATUS_RESERVED if active_exists else STATUS_AVAILABLE
        setattr(car, "status", status_value)  # bypass CharField descriptor static type misjudgment
        car.save()

    def place_order_and_pay(
        self, *,
        actor_user_id: int,      # acting user = booking user
        user_id: int,            # owner of booking
        car_id: int,
        start_str: str, end_str: str,
        pay_method: str,         # paypal/stripe/creditcard/banktransfer/crypto/googlepay
        pay_kwargs: dict         # gateway-specific params
    ) -> Booking:
        """
        One-shot place order + pay (persist only on success)
        Process:
          1) validate profile, date range, car availability; quote
          2) call payment gateway (no DB writes yet)
          3) Booking(pending) + Payment(ok=True)；on success, persist Booking(pending) + Payment(ok=True) + set car to reserved
          4) write audit log
        """
        # 1) validate & quote
        start = self._parse_date(start_str)
        end = self._parse_date(end_str)
        if end < start:
            raise ValidationError("End date cannot be earlier than start date")

        car = Car.get_or_none(Car.id == car_id)
        if not car:
            raise NotFoundError("Car not found")
        prof = CustomerProfile.get_or_none(CustomerProfile.user == user_id)
        if not prof:
            raise ConflictError("Profile required before booking")

        # consider pending+confirmed as taken
        conflict = Booking.select().where(
            (Booking.car == car) &
            (Booking.status.in_([BOOKING_PENDING, BOOKING_CONFIRMED])) &
            (Booking.start_date <= end) &
            (Booking.end_date >= start)
        ).exists()
        if conflict:
            raise ConflictError("Slot already taken")

        # quote (picks only the best single rule)
        days = (end - start).days + 1
        base_cost, adjs, grand_total, daily_rate = self.pricing.quote(car=car, start_date=start, end_date=end)

        # 2) call payment gateway (no DB writes yet)
        req = PaymentRequest(amount=grand_total, currency="NZD", payer_id=str(actor_user_id))
        gw = PaymentGateway()
        result = gw.process(pay_method, req, **(pay_kwargs or {}))

        if not result.ok:
            # on failure, do not persist anything
            raise ConflictError(f"Payment failed: {result.message or 'unknown'}")

        # 3) in transaction: Booking(pending) + Payment(ok=True) + set car to reserved
        db = DatabaseManager().db
        try:
            with db.atomic():
                b = Booking.create(
                    car=car, user=user_id,
                    start_date=start, end_date=end,
                    status=BOOKING_PENDING,      # paid then pending review
                    days=days,
                    base_daily_rate=daily_rate,
                    base_cost=base_cost,
                    adj_total=sum(d for _, d in adjs),
                    grand_total=grand_total,
                    snap_first_name=prof.first_name,
                    snap_last_name=prof.last_name,
                    snap_phone=prof.phone,
                    snap_id_document=prof.id_document
                )
                # persist payment record
                Payment.create(
                    booking=b, method=pay_method, amount=grand_total,
                    currency="NZD", ok=True, message=result.message, txn_id=result.txn_id
                )
                # set car to reserved
                self._recompute_car_status(car)

                # audit
                self.audit.write(actor_user_id=actor_user_id, action="create_payment",
                                 target_type="payment", target_id=b.id,   # could also use payment.id here
                                 detail=f"booking#{b.id} {pay_method} ok=True txn={result.txn_id or ''}")
                self.audit.write(actor_user_id=actor_user_id, action="create_booking",
                                 target_type="booking", target_id=b.id,
                                 detail=f"car={car.id} {start_str}->{end_str} pending(after-paid)")
                return b
        except Exception as e:
            raise DatabaseError(f"Failed to create booking after payment: {e}") from e