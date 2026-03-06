from django.urls import path
from finance.views import confirm_payment, failed_payment


urlpatterns = [
    path('fail/<str:invoice_order_id>/', failed_payment, name='payment_failed'),
    path('confirm/<str:invoice_order_id>/', confirm_payment, name='payment_success'),
]
