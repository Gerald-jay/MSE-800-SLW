# admin_service/pricing_service.py
# -*- coding: utf-8 -*-
from datetime import datetime
from typing import List, Optional, Tuple, cast
from db.db_manager import DatabaseManager
from db.models import PricingRule, Car, PRULE_DISCOUNT, PRULE_SURCHARGE, AMOUNT_PERCENT, AMOUNT_FIXED, STATUS_AVAILABLE
from common.validators import Validator
from common.exceptions import ValidationError, NotFoundError, DatabaseError
from admin_service.audit_service import AuditService

DATE_FMT = "%d-%m-%Y"

class PricingService:
    def __init__(self, audit: Optional[AuditService] = None):
        db = DatabaseManager().db
        db.create_tables([PricingRule])
        self.audit = audit or AuditService()

    @staticmethod
    def _parse_date_or_none(s: Optional[str]):
        if not s:
            return None
        try:
            return datetime.strptime(s, DATE_FMT).date()
        except ValueError:
            raise ValidationError(f"Invalid date format {DATE_FMT}")

    def create_rule(self, *, actor_user_id: int, name: str, rule_type: str, amount_type: str, amount_value: float,
                    scope: str = "global", car_id: Optional[int] = None, min_days: int = 1,
                    start_date_str: Optional[str] = None, end_date_str: Optional[str] = None) -> PricingRule:
        # 校验/validate
        Validator.validate_name(name, "Rule name", 80)
        Validator.validate_rule_type(rule_type)
        Validator.validate_amount_type(amount_type)
        Validator.validate_amount(amount_value)
        if scope not in ("global", "car"):
            raise ValidationError("scope must be either 'global' or 'car'")
        if min_days <= 0:
            raise ValidationError("min_days must be ≥ 1")

        start_date = self._parse_date_or_none(start_date_str)
        end_date = self._parse_date_or_none(end_date_str)
        if start_date and end_date and end_date < start_date:
            raise ValidationError("End date cannot be earlier than start date")

        car = None
        if scope == "car":
            car = Car.get_or_none(Car.id == car_id)
            if not car:
                raise NotFoundError(f"Car not found: ID={car_id}")

        try:
            rule = PricingRule.create(
                name=name.strip(),
                rule_type=rule_type,
                amount_type=amount_type,
                amount_value=amount_value,
                scope=scope,
                car=car,
                min_days=min_days,
                start_date=start_date,
                end_date=end_date,
                is_active=True
            )
            self.audit.write(actor_user_id=actor_user_id, action="create_pricing_rule",
                             target_type="pricing_rule", target_id=rule.id,
                             detail=f"{rule_type} {amount_type} {amount_value} scope={scope} min_days={min_days}")
            return rule
        except Exception as e:
            raise DatabaseError(f"Failed to create pricing rule: {e}") from e

    def list_rules(self) -> List[PricingRule]:
        return list(PricingRule.select().order_by(PricingRule.id.desc()))

    def set_active(self, *, actor_user_id: int, rule_id: int, active: bool) -> PricingRule:
        rule = PricingRule.get_or_none(PricingRule.id == rule_id)
        if not rule:
            raise NotFoundError("Rule not found")
        rule.is_active = active
        rule.save()
        self.audit.write(actor_user_id=actor_user_id, action="update_pricing_rule",
                         target_type="pricing_rule", target_id=rule.id,
                         detail=f"set_active={active}")
        return rule

    # Calculate quote: returns (base_cost, adjustments: List[(rule_id, delta)], grand_total)
    def quote(self, *, car: Car, start_date, end_date) -> Tuple[float, List[Tuple[int, float]], float, float]:
        days = (end_date - start_date).days + 1
        daily_rate: float = cast(float, car.daily_rate)
        base_cost = daily_rate * days

        # 1) Filter applicable rules
        q = (PricingRule
            .select()
            .where(
                (PricingRule.is_active == True) &
                ((PricingRule.scope == "global") | ((PricingRule.scope == "car"))) &
                ((PricingRule.start_date.is_null(True)) | (PricingRule.start_date <= start_date)) &
                ((PricingRule.end_date.is_null(True))   | (PricingRule.end_date >= end_date)) &
                (PricingRule.min_days <= days)
            ))

        # 2) Calculate delta for each rule, but do not stack; only pick 1 "main rule"
        best_discount: tuple[int, float] | None = None  # (rule_id, delta<0)
        best_surcharge: tuple[int, float] | None = None # (rule_id, delta>0)

        for rule in q:
            # Calculate the amount adjustment for this rule
            if rule.amount_type == AMOUNT_PERCENT:
                raw = base_cost * (rule.amount_value / 100.0)
            else:  # AMOUNT_FIXED
                raw = float(rule.amount_value)

            delta = -abs(raw) if rule.rule_type == PRULE_DISCOUNT else abs(raw)

            # Record the "strongest" discount/surcharge
            if rule.rule_type == PRULE_DISCOUNT:
                if (best_discount is None) or (delta < best_discount[1]):  # more negative => bigger discount
                    best_discount = (rule.id, delta)
            else:  # surcharge
                if (best_surcharge is None) or (delta > best_surcharge[1]):  # more positive => bigger surcharge
                    best_surcharge = (rule.id, delta)

        # 3) Pick the "main rule": prefer discount if any; else use surcharge; else no adjustment
        chosen: List[Tuple[int, float]] = []
        if best_discount is not None:
            chosen = [best_discount]
        elif best_surcharge is not None:
            chosen = [best_surcharge]

        grand_total = base_cost + (chosen[0][1] if chosen else 0.0)
        return base_cost, chosen, grand_total, daily_rate
