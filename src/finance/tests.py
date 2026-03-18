from decimal import Decimal
from datetime import datetime
from zoneinfo import ZoneInfo
from unittest.mock import patch

from django.test import SimpleTestCase

from finance.models import InvoiceTossPayments
from finance.views import _build_confirm_error_message, _confirmation_window_expired


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


class ConfirmPaymentHelpersTests(SimpleTestCase):
    def test_confirmation_window_expired_after_ten_minutes(self):
        payment_data = {"requestedAt": "2026-03-18T22:19:43+09:00"}
        mocked_now = datetime(2026, 3, 18, 17, 2, 36, tzinfo=ZoneInfo("Europe/Moscow"))

        with patch("finance.views.timezone.now", return_value=mocked_now):
            self.assertTrue(_confirmation_window_expired(payment_data))

    def test_build_confirm_error_message_for_expired_in_progress_payment(self):
        payment_data = {"status": "IN_PROGRESS", "requestedAt": "2026-03-18T22:19:43+09:00"}
        mocked_now = datetime(2026, 3, 18, 17, 2, 36, tzinfo=ZoneInfo("Europe/Moscow"))

        with patch("finance.views.timezone.now", return_value=mocked_now):
            message = _build_confirm_error_message("Base error", payment_data)

        self.assertIn("10-минутное окно подтверждения уже истекло", message)

    def test_build_confirm_error_message_for_fresh_in_progress_payment(self):
        payment_data = {"status": "IN_PROGRESS", "requestedAt": "2026-03-18T22:19:43+09:00"}
        mocked_now = datetime(2026, 3, 18, 16, 21, 0, tzinfo=ZoneInfo("Europe/Moscow"))

        with patch("finance.views.timezone.now", return_value=mocked_now):
            message = _build_confirm_error_message("Base error", payment_data)

        self.assertIn("Повторите подтверждение через несколько секунд", message)
