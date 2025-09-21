# controllers/admin_pricing_cli.py
# -*- coding: utf-8 -*-
from admin_service.pricing_service import PricingService, DATE_FMT
from common.input_utils import prompt_str, prompt_choice, prompt_float, prompt_int, prompt_id, prompt_date

class AdminPricingCLI:
    def __init__(self, svc: PricingService, current_user_id: int):
        self.svc = svc
        self.uid = current_user_id

    def show(self):
        while True:
            print("""
=== Pricing Rules ===
1) Create rule
2) Enable/Disable
3) List rules
0) Back
""")
            c = input("Choose: ").strip()
            if c == "1":
                self._create()
            elif c == "2":
                self._toggle()
            elif c == "3":
                self._list()
            elif c == "0":
                break
            else:
                print("Invalid choice")

    def _create(self):
        name = prompt_str("Rule name")
        rule_type = prompt_choice("Rule type", ["discount","surcharge"], "discount")
        amt_type = prompt_choice("Amount type", ["percent","fixed"], "percent")
        amt_val = prompt_float("Amount value")
        scope = prompt_choice("Scope", ["global","car"], "global")
        car_id = None
        if scope == "car":
            car_id = prompt_id("Car ID")
            if car_id is None:
                return
        min_days = prompt_int("Min days", 1)
        use_date = input("Set effective date? Y/n (default n): ").strip().lower()
        start = end = None
        if use_date == "y":
            start = prompt_date("Start", fmt=DATE_FMT)
            end = prompt_date("End", fmt=DATE_FMT)
        try:
            r = self.svc.create_rule(actor_user_id=self.uid, name=name, rule_type=rule_type,
                                     amount_type=amt_type, amount_value=amt_val,
                                     scope=scope, car_id=car_id, min_days=min_days,
                                     start_date_str=start, end_date_str=end)
            print(f"✓ Created rule #{r.id}")
        except Exception as e:
            print("✗ Failed to create rule:", e)

    def _toggle(self):
        rid = prompt_id("Rule ID")
        if rid is None: return
        active = input("Enable? Y/n (default Y): ").strip().lower() != "n"
        try:
            r = self.svc.set_active(actor_user_id=self.uid, rule_id=rid, active=active)
            print(f"✓ #{r.id} active={r.is_active}")
        except Exception as e:
            print("✗ Failed to toggle rule:", e)

    def _list(self):
        rules = self.svc.list_rules()
        if not rules:
            print("No rules")
            return
        for r in rules:
            car_scope = f"car#{r.car.id}" if (r.scope == 'car' and r.car) else "global"
            print(f"#{r.id} [{ 'ON' if r.is_active else 'OFF' }] {r.name} | {r.rule_type}/{r.amount_type}={r.amount_value} | scope={car_scope} | min_days={r.min_days} | {r.start_date or '-'}~{r.end_date or '-'}")
