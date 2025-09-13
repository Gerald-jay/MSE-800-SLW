1. I implemented a payment processing system that supports CreditCard, PayPal, BankTransfer, Crypto, GooglePay.

2. Factory Pattern is used to dynamically create payment method objects via a registry-based factory (PaymentFactory.create(key, **kwargs)). Adding a new method only requires registering the class—no changes to the client or gateway.

3. Singleton Pattern is used for the PaymentGateway, ensuring a single entry point manages cross-cutting concerns (logging, retries, idempotency, metrics) and shared state.

4. Each payment method implements a common PaymentMethod interface (strategy), keeping the client decoupled from concrete classes.