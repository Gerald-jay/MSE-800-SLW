from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from threading import Lock
from typing import Type, Dict, Any

# -------- Domain ----------
@dataclass(frozen=True)
class PaymentRequest:
    amount: float
    currency: str
    payer_id: str

@dataclass(frozen=True)
class PaymentResult:
    ok: bool
    message: str
    txn_id: str | None = None

# -------- Strategy interface ----------
class PaymentMethod(ABC):
    @abstractmethod
    def pay(self, req: PaymentRequest) -> PaymentResult: ...

# -------- Concrete methods ----------
class PayPalPayment(PaymentMethod):
    def __init__(self, email: str): self.email = email
    def pay(self, req: PaymentRequest) -> PaymentResult:
        return PaymentResult(True, f"PayPal({self.email}) paid {req.amount} {req.currency}", f"PP-{req.payer_id}-001")

class StripePayment(PaymentMethod):
    def __init__(self, customer_id: str): self.customer_id = customer_id
    def pay(self, req: PaymentRequest) -> PaymentResult:
        return PaymentResult(True, f"Stripe({self.customer_id}) paid {req.amount} {req.currency}", f"ST-{req.payer_id}-002")

class CreditCardPayment(PaymentMethod):
    def __init__(self, card_no: str, cvv: str, exp: str):
        self.card_no, self.cvv, self.exp = card_no, cvv, exp
    def pay(self, req: PaymentRequest) -> PaymentResult:
        return PaymentResult(True, f"CreditCard(**{self.card_no[-4:]}) paid {req.amount} {req.currency}", f"CC-{req.payer_id}-003")

class BankTransferPayment(PaymentMethod):
    def __init__(self, iban: str): self.iban = iban
    def pay(self, req: PaymentRequest) -> PaymentResult:
        return PaymentResult(True, f"BankTransfer({self.iban[:6]}...) sent {req.amount} {req.currency}", f"BT-{req.payer_id}-004")

class CryptoPayment(PaymentMethod):
    def __init__(self, wallet: str, network: str = "ETH"):
        self.wallet, self.network = wallet, network
    def pay(self, req: PaymentRequest) -> PaymentResult:
        return PaymentResult(True, f"Crypto({self.network}) {req.amount} {req.currency} from {self.wallet[:6]}...", f"CR-{req.payer_id}-005")

class GooglePayPayment(PaymentMethod):
    def __init__(self, token: str): self.token = token
    def pay(self, req: PaymentRequest) -> PaymentResult:
        return PaymentResult(True, f"GooglePay token({self.token[:6]}...) paid {req.amount} {req.currency}", f"GP-{req.payer_id}-006")

# -------- Factory ----------
class PaymentFactory:
    _registry: Dict[str, Type[PaymentMethod]] = {}

    @classmethod
    def register(cls, key: str, payment_cls: Type[PaymentMethod]) -> None:
        cls._registry[key.lower()] = payment_cls

    @classmethod
    def create(cls, key: str, **kwargs) -> PaymentMethod:
        k = key.lower()
        if k not in cls._registry:
            raise ValueError(f"Unknown payment method: {key}")
        return cls._registry[k](**kwargs)

# register all methods
PaymentFactory.register("paypal", PayPalPayment)
PaymentFactory.register("stripe", StripePayment)
PaymentFactory.register("creditcard", CreditCardPayment)
PaymentFactory.register("banktransfer", BankTransferPayment)
PaymentFactory.register("crypto", CryptoPayment)
PaymentFactory.register("googlepay", GooglePayPayment)

# -------- Singleton Gateway ----------
class PaymentGateway:
    _instance: "PaymentGateway | None" = None
    _lock = Lock()

    def __new__(cls):
        if cls._instance is None:
            with cls._lock:
                if cls._instance is None:
                    cls._instance = super().__new__(cls)
        return cls._instance

    def process(self, method_key: str, req: PaymentRequest, **init_kwargs) -> PaymentResult:
        method = PaymentFactory.create(method_key, **init_kwargs)
        # note that cross-cutting concerns can be handled here: logging, retries, risk control, idempotency, metrics...
        return method.pay(req)

# -------- Demo / client code ----------
if __name__ == "__main__":
    gw = PaymentGateway()                     # singleton entry point
    req = PaymentRequest(amount=99.0, currency="NZD", payer_id="u1001")

    print(gw.process("paypal", req, email="buyer@example.com"))
    print(gw.process("stripe", req, customer_id="cus_123"))
    print(gw.process("creditcard", req, card_no="4111111111111111", cvv="123", exp="09/26"))
    print(gw.process("banktransfer", req, iban="DE89370400440532013000"))
    print(gw.process("crypto", req, wallet="0xabc123...def", network="ETH"))
    print(gw.process("googlepay", req, token="tok_live_abcxyz"))
