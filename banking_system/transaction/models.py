from django.db import models

# Create your models here.
from accounts.models import UserBankAccount
from .constrants import TRANSACTION_TYPE

class Transaction(models.Model):
    transaction_account = models.ForeignKey(UserBankAccount,related_name='transaction_amount',on_delete=models.CASCADE)
    amount = models.DecimalField(decimal_places=2, max_digits=12)
    balance_after_transaction = models.DecimalField(decimal_places=2, max_digits = 12)
    transaction_type = models.IntegerField(choices=TRANSACTION_TYPE, null=True)
    timestamp = models.DateField(auto_now_add=True)
    loan_approve = models.BooleanField(default=False)

    class Meta:
        ordering=['timestamp']
        



