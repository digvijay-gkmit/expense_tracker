from django.db import models
from users.models import CustomUser
from categories.models import Category
import uuid
from django.utils import timezone
from base.models import BaseModel

class Transaction(BaseModel):
    
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True,max_length=255)
    date = models.DateField(default=timezone.now)
    PAYMENT_METHOD_CHOICES = [
        ("online", "Online"),
        ("cash", "Cash"),
    ]
    payment_method = models.CharField(max_length=10, choices=PAYMENT_METHOD_CHOICES)

    TRANSACTION_TYPE_CHOICES = [
        ("debit", "Debit"),
        ("credit", "Credit"),
    ]
    transaction_type = models.CharField(max_length=6, choices=TRANSACTION_TYPE_CHOICES)

    user = models.ForeignKey(CustomUser, on_delete=models.DO_NOTHING, related_name="transactions")
    category = models.ForeignKey(Category,on_delete=models.SET_NULL,null=True,
        blank=True,
        related_name="transactions",
    )

    def __str__(self):
        return f"Transaction {self.id} - {self.transaction_type} - {self.amount}"

    class Meta:
        verbose_name = "Transaction"
        verbose_name_plural = "Transactions"



