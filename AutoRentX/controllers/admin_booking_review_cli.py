# controllers/admin_booking_review_cli.py 〔新增 / new file〕
# -*- coding: utf-8 -*-
from admin_service.booking_review_service import BookingReviewService
from common.input_utils import prompt_id, prompt_choice

class AdminBookingReviewCLI:
    def __init__(self, svc: BookingReviewService, current_user_id: int):
        self.svc = svc
        self.uid = current_user_id

    def show(self):
        while True:
            print("""
=== Booking Review ===
1) List pending
2) Review (approve/reject)
0) Back
""")
            c = input("Choose: ").strip()
            if c == "1":
                self._list_pending()
            elif c == "2":
                self._review()
            elif c == "0":
                break
            else:
                print("Invalid choice")

    def _list_pending(self):
        rows = self.svc.list_pending()
        if not rows:
            print("No pending bookings")
            return
        for b in rows:
            print(f"#{b.id} user#{b.user.id}({b.snap_first_name} {b.snap_last_name}) phone#{b.snap_phone} car#{b.car.id} {b.car.make} {b.car.model} "
                  f"{b.start_date}~{b.end_date} total={b.grand_total:.2f}")

    def _review(self):
        bid = prompt_id("Booking ID")
        if bid is None: return
        decision = prompt_choice("Decision", ["approve","reject"], "approve")
        try:
            if decision == "approve":
                b = self.svc.approve(actor_user_id=self.uid, booking_id=bid)
                print(f"✓ Approved: #{b.id}")
            else:
                b = self.svc.reject(actor_user_id=self.uid, booking_id=bid)
                print(f"✓ Rejected: #{b.id}")
        except Exception as e:
            print("✗ Error:", e)
