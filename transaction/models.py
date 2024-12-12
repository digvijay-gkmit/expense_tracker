from django.db import models
from user.models import CustomUser
import uuid


class Transaction(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    user = models.ForeignKey(
        "CustomUser", on_delete=models.CASCADE, related_name="transactions"
    )

    amount = models.DecimalField(max_digits=10, decimal_places=2)

    description = models.TextField()

    category = models.ForeignKey(
        "Category",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="transactions",
    )
    date = models.DateTimeField()

    PAYMENT_METHOD_CHOICES = [
        ("online", "Online"),
        ("cash", "Cash"),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    TRANSACTION_TYPE_CHOICES = [
        ("debit", "Debit"),
        ("credit", "Credit"),
    ]
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE_CHOICES)

    def __str__(self):
        return f"Transaction {self.id} - {self.transaction_type} - {self.amount}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"



