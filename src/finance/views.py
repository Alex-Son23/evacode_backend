from decimal import Decimal, InvalidOperation

import requests
from django.conf import settings
from django.http import HttpResponseNotAllowed
from django.shortcuts import render
from requests.auth import HTTPBasicAuth
from finance.models import InvoiceTossPayments


def _default_home_url():
    return getattr(settings, "EVACODE_FRONTEND_URL", "https://www.evacode.org")


def _parse_error(response):
    try:
        data = response.json()
    except ValueError:
        return f"HTTP_{response.status_code}", response.text or "Unknown error"

    return data.get("code", f"HTTP_{response.status_code}"), data.get("message", response.text or "Unknown error")


def _normalize_amount(raw_amount, invoice):
    amount_value = raw_amount if raw_amount not in (None, "") else (invoice.amount if invoice else None)
    if amount_value is None:
        return None

    try:
        decimal_amount = Decimal(str(amount_value))
    except InvalidOperation:
        return None

    if decimal_amount == decimal_amount.to_integral():
        return int(decimal_amount)
    return float(decimal_amount)


def _render_failed(request, invoice, order_id, code, message):
    context = {
        "home_url": _default_home_url(),
        "invoice": invoice,
        "order_id": order_id,
        "error_code": code,
        "error_message": message,
    }
    return render(request, "finance/payment_failed.html", context)


def confirm_payment(request, invoice_order_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    invoice = InvoiceTossPayments.objects.filter(order_id=invoice_order_id).first()
    if not invoice:
        return _render_failed(
            request=request,
            invoice=None,
            order_id=invoice_order_id,
            code="INVOICE_NOT_FOUND",
            message="Инвойс для подтверждения не найден.",
        )

    payment_key = request.GET.get("paymentKey") or invoice.payment_id
    confirm_amount = _normalize_amount(request.GET.get("amount"), invoice)

    if not payment_key or confirm_amount is None:
        return _render_failed(
            request=request,
            invoice=invoice,
            order_id=invoice_order_id,
            code="MISSING_CONFIRM_PARAMS",
            message="Не хватает параметров paymentKey или amount для подтверждения оплаты.",
        )

    if not (invoice.is_paid and invoice.status == "DONE"):
        try:
            response = requests.post(
                url="https://api.tosspayments.com/v1/payments/confirm",
                json={
                    "paymentKey": payment_key,
                    "orderId": invoice_order_id,
                    "amount": confirm_amount,
                },
                auth=HTTPBasicAuth(settings.TOSS_SECRET_KEY, ""),
                timeout=20,
            )
        except requests.RequestException as exc:
            invoice.status = "FAILED"
            invoice.is_paid = False
            invoice.save(update_fields=["status", "is_paid", "updated_at"])
            return _render_failed(
                request=request,
                invoice=invoice,
                order_id=invoice_order_id,
                code="CONFIRM_REQUEST_ERROR",
                message=f"Ошибка запроса к платёжному шлюзу: {exc}",
            )

        if not response.ok:
            error_code, error_message = _parse_error(response)
            if error_code == "ALREADY_PROCESSED_PAYMENT":
                invoice.payment_id = payment_key
                invoice.status = "DONE"
                invoice.is_paid = True
                invoice.save(update_fields=["payment_id", "status", "is_paid", "updated_at"])
            else:
                invoice.status = "FAILED"
                invoice.is_paid = False
                invoice.save(update_fields=["status", "is_paid", "updated_at"])
                return _render_failed(
                    request=request,
                    invoice=invoice,
                    order_id=invoice_order_id,
                    code=error_code,
                    message=error_message,
                )
        else:
            data = response.json()
            invoice.payment_id = data.get("paymentKey", payment_key)
            invoice.status = data.get("status", invoice.status)
            invoice.is_paid = invoice.status == "DONE"
            invoice.save(update_fields=["payment_id", "status", "is_paid", "updated_at"])

    context = {
        "home_url": _default_home_url(),
        "invoice": invoice,
        "order_id": invoice_order_id,
        "payment_key": payment_key,
        "amount": request.GET.get("amount") or invoice.amount,
    }
    return render(request, "finance/payment_success.html", context)


def failed_payment(request, invoice_order_id):
    if request.method != "GET":
        return HttpResponseNotAllowed(["GET"])

    order_id = request.GET.get("orderId") or invoice_order_id
    invoice = InvoiceTossPayments.objects.filter(order_id=order_id).first()
    error_code = request.GET.get("code", "PAYMENT_FAILED")
    error_message = request.GET.get("message", "Не удалось завершить оплату. Попробуйте ещё раз позже.")
    payment_key = request.GET.get("paymentKey") or (invoice.payment_id if invoice else None)

    if invoice:
        was_paid = bool(invoice.is_paid or invoice.status == "DONE")

        invoice.is_paid = False
        invoice.status = "CANCELED" if error_code in {"PAY_PROCESS_CANCELED", "USER_CANCEL", "PAYMENT_CANCELED"} else "FAILED"
        invoice.save(update_fields=["status", "is_paid", "updated_at"])

        if was_paid and payment_key:
            try:
                cancel_response = requests.post(
                    url=f"https://api.tosspayments.com/v1/payments/{payment_key}/cancel",
                    json={"cancelReason": "User reached fail callback page"},
                    auth=HTTPBasicAuth(settings.TOSS_SECRET_KEY, ""),
                    timeout=20,
                )
            except requests.RequestException as exc:
                error_code = "CANCEL_REQUEST_ERROR"
                error_message = f"{error_message} Ошибка запроса отмены: {exc}"
            else:
                if cancel_response.ok:
                    cancel_data = cancel_response.json()
                    invoice.status = cancel_data.get("status", "CANCELED")
                    invoice.is_paid = False
                    invoice.save(update_fields=["status", "is_paid", "updated_at"])
                else:
                    cancel_code, cancel_message = _parse_error(cancel_response)
                    error_code = f"{error_code} | {cancel_code}"
                    error_message = f"{error_message} Отмена не выполнена: {cancel_message}"

    context = {
        "home_url": _default_home_url(),
        "invoice": invoice,
        "order_id": order_id,
        "error_code": error_code,
        "error_message": error_message,
    }
    return render(request, "finance/payment_failed.html", context)
