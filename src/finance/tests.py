from decimal import Decimal

from django.test import SimpleTestCase

from finance.models import InvoiceTossPayments


class InvoiceTossPaymentsPayloadTests(SimpleTestCase):
    def _build_invoice(self, payment_type):
        return InvoiceTossPayments(
            amount=Decimal("10.00"),
            description="EVACODE Order",
            customer_name="Test User",
            customer_phone="+70000000000",
            customer_email="test@example.com",
            manager_name="Manager",
            payment_link="",
            payment_type=payment_type,
        )

    def test_card_payment_type_builds_card_payload(self):
        invoice = self._build_invoice(InvoiceTossPayments.PaymentType.CARD)

        payload = invoice._build_toss_payload(
            order_id="inv-1",
            success_url="https://example.com/success",
            fail_url="https://example.com/fail",
        )

        self.assertEqual(payload["method"], InvoiceTossPayments.PaymentType.CARD)
        self.assertNotIn("provider", payload)
        self.assertNotIn("currency", payload)

    def test_foreign_payment_type_builds_paypal_payload(self):
        invoice = self._build_invoice(InvoiceTossPayments.PaymentType.FOREIGN)

        payload = invoice._build_toss_payload(
            order_id="inv-2",
            success_url="https://example.com/success",
            fail_url="https://example.com/fail",
        )

        self.assertEqual(payload["method"], InvoiceTossPayments.PaymentType.FOREIGN)
        self.assertEqual(payload["provider"], "PAYPAL")
        self.assertEqual(payload["currency"], "USD")

    def test_unsupported_payment_type_raises_error(self):
        invoice = self._build_invoice("BANK_TRANSFER")

        with self.assertRaisesMessage(ValueError, "Unsupported TOSS payment type"):
            invoice._build_toss_payload(
                order_id="inv-3",
                success_url="https://example.com/success",
                fail_url="https://example.com/fail",
            )
