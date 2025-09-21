# common/payment_app.py
# -*- coding: utf-8 -*-
"""
Mock Payment Gateway (for CLI project)

unified interface: PaymentRequest + PaymentGateway.process()
support multiple methods: paypal, stripe, creditcard, banktransfer, crypto, googlepay
"""

from dataclasses import dataclass
from typing import Optional
import uuid
import random

# ----------------------------
# Data structures
# ----------------------------

@dataclass
class PaymentRequest:
    """Payment request"""
    amount: float            # payment amount
    currency: str            # currency code (e.g., NZD)
    payer_id: str            # payer identifier (user ID or email)


@dataclass
class PaymentResult:
    """Payment result"""
    ok: bool                 # success or not
    message: Optional[str]   # message from gateway
    txn_id: Optional[str]    # transaction ID


# ----------------------------
# Gateway implementation
# ----------------------------

class PaymentGateway:
    """
    Mock payment gateway
    supports multiple payment methods, each generates a mock txn_id
    """

    def process(self, method: str, req: PaymentRequest, **kwargs) -> PaymentResult:
        """
        Execute a payment

        :param method: payment method (paypal/stripe/creditcard/banktransfer/crypto/googlepay)
        :param req: PaymentRequest object
        :param kwargs: other parameters (varies by payment method, e.g., email, card_no, wallet, etc.)
        :return: PaymentResult
        """
        method = method.lower()

        # simulate failure chance
        fail_chance = 0.01  # 1% chance
        if random.random() < fail_chance:
            return PaymentResult(
                ok=False,
                message=f"Simulated failure for {method}",
                txn_id=None
            )

        # generate transaction id
        txn_id = f"{method.upper()}-{uuid.uuid4().hex[:12]}"

        # per-method message
        if method == "paypal":
            msg = f"success for {kwargs.get('email', req.payer_id)}"
        elif method == "stripe":
            msg = f"Stripe {kwargs.get('customer_id', req.payer_id)} success"
        elif method == "creditcard":
            masked = str(kwargs.get("card_no", "****"))[-4:]
            msg = f"credit card ****{masked} success"
        elif method == "banktransfer":
            msg = f"{kwargs.get('iban','')} bank transfer success"
        elif method == "crypto":
            msg = f"{kwargs.get('wallet','')} crypto wallet success"
        elif method == "googlepay":
            msg = f"Google Pay token success"
        else:
            msg = f"Unknown method: {method}"

        return PaymentResult(ok=True, message=msg, txn_id=txn_id)
