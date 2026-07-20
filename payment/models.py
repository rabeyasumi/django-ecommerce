from django.db import models
from order.models import Order


class Payment(models.Model):
    PAYMENT_STATUS = (
        ('Pending', 'Pending'),
        ('Paid', 'Paid'),
        ('Failed', 'Failed'),
        ('Cancelled', 'Cancelled'),
    )

    order = models.OneToOneField(
        Order,
        on_delete=models.CASCADE,
        related_name='payment'
    )

    transaction_id = models.CharField(
        max_length=255,
        unique=True,
        null=True,
        blank=True
    )

    amount = models.DecimalField(
        max_digits=10,
        decimal_places=2
    )

    payment_method = models.CharField(
        max_length=50,
        default='SSLCommerz'
    )

    status = models.CharField(
        max_length=20,
        choices=PAYMENT_STATUS,
        default='Pending'
    )

    created_at = models.DateTimeField(
        auto_now_add=True
    )

    updated_at = models.DateTimeField(
        auto_now=True
    )

    def __str__(self):
        return f"{self.order.id} - {self.status}"