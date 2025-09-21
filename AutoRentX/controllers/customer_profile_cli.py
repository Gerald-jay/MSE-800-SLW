# controllers/customer_profile_cli.py
# -*- coding: utf-8 -*-
from customer_service.profile_service import ProfileService
from common.input_utils import prompt_str

class CustomerProfileCLI:
    def __init__(self, svc: ProfileService, current_user_id: int):
        self.svc = svc
        self.uid = current_user_id

    def show(self):
        p = self.svc.get_my_profile(self.uid)
        if not p:
            print("No profile yet, please create.")
            self._create_or_update()
        else:
            print(f"Current profile: {p.first_name} {p.last_name} | {p.phone} | {p.id_document}")
            act = input("Modify? Y/n (default n): ").strip().lower()
            if act == "y":
                self._create_or_update()

    def _create_or_update(self):
        fn = prompt_str("First name")
        ln = prompt_str("Last name")
        ph = prompt_str("Phone")
        idd = prompt_str("ID Document")
        try:
            p = self.svc.create_or_update(actor_user_id=self.uid, user_id=self.uid, first_name=fn, last_name=ln, phone=ph, id_document=idd)
            print(f"✓ Saved. #{p.id}")
        except Exception as e:
            print("✗ Failed to create or update profile:", e)
