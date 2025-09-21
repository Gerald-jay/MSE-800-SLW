# controllers/customer_rent_cli.py
# -*- coding: utf-8 -*-
from customer_service.rent_service import RentService
from customer_service.profile_service import ProfileService
from common.input_utils import prompt_choice, prompt_id, prompt_date_range, prompt_str

class CustomerRentCLI:
    def __init__(self, rent_svc: RentService, profile_svc: ProfileService, current_user_id: int):
        self.rent = rent_svc
        self.profile = profile_svc
        self.uid = current_user_id

    def show(self):
        while True:
            print("""
=== Rent ===
1) Available cars by date
2) Select car & place order
3) My bookings
0) Back
""")
            c = input("Choose: ").strip()
            if c == "1":
                self._list_available()
            elif c == "2":
                self._place_order()
            elif c == "3":
                self._my_bookings()
            elif c == "0":
                break
            else:
                print("Invalid choice")

    def _list_available(self):
        start, end = prompt_date_range("Start date", "End date")
        try:
            cars = self.rent.available_cars(start, end)
            if not cars:
                print("No available cars")
                return
            for c in cars:
                print(f"#{c.id} {c.make} {c.model} {c.year} | ${c.daily_rate}/day")
        except Exception as e:
            print("✗ Error:", e)

    def _my_bookings(self):
        rows = self.rent.list_my_bookings(self.uid)
        if not rows:
            print("No bookings yet")
            return
        for b in rows:
            print(f"#{b.id} car#{b.car.id} {b.car.make} {b.car.model} "
                  f"{b.start_date}~{b.end_date} | status={b.status} | total={b.grand_total:.2f}")

    def _place_order(self):
    # 1) Profile check
        p = self.profile.get_my_profile(self.uid)
        if not p:
            print("✗ Complete your profile first")
            return

        # 2) Car + dates
        car_id = prompt_id("Car ID")
        if car_id is None: return
        start, end = prompt_date_range("Start date", "End date")

        # 3) Quote (for display only; final amount is calculated server-side)
        try:
            days, base_cost, adjs, total, daily_rate = self.rent.quote(car_id, start, end)
            unit = "day" if days == 1 else "days"
            print(f"Quote: {days} {unit} x daily_rate = {base_cost:.2f}")
            if adjs:
                for rid, delta in adjs:
                    print(f"  Rule #{rid}: {'+' if delta>=0 else ''}{delta:.2f}")
            print(f"Total: {total:.2f}")
        except Exception as e:
            print("✗ Error:", e)
            return

        # 4) choose payment method and pay now
        ok = input("Do you want to continue and pay? Y/n (default Y): ").strip().lower()
        if ok == "n":
            return

        method = prompt_choice("Method",
                            ["paypal","stripe","creditcard","banktransfer","crypto","googlepay"],
                            "paypal")
        kwargs = {}
        if method == "paypal":
            kwargs["email"] = prompt_str("PayPal Email")
        elif method == "stripe":
            kwargs["customer_id"] = prompt_str("Stripe Customer ID")
        elif method == "creditcard":
            kwargs["card_no"] = prompt_str("Card Number")
            kwargs["cvv"] = prompt_str("CVV")
            kwargs["exp"] = prompt_str("Expiry (MM/YY)")
        elif method == "banktransfer":
            kwargs["iban"] = prompt_str("IBAN")
        elif method == "crypto":
            kwargs["wallet"] = prompt_str("Wallet")
            kwargs["network"] = prompt_str("Network (e.g., ETH)")
        elif method == "googlepay":
            kwargs["token"] = prompt_str("Token")

        # 5) one-shot place + pay
        try:
            b = self.rent.place_order_and_pay(
                actor_user_id=self.uid, user_id=self.uid,
                car_id=car_id, start_str=start, end_str=end,
                pay_method=method, pay_kwargs=kwargs
            )
            print(f"✓ Payment completed, booking created (pending): #{b.id}")
        except Exception as e:
            print("✗ Error:", e)
