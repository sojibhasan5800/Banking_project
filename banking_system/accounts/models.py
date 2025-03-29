from django.db import models
from django.contrib.auth.models import User
from .constants import ACCOUNT_TYPE, GENDER_TYPE

# Create your models here.
class UserBankAccount(models.Model):
    user = models.OneToOneField(User,related_name='user_account', on_delete=models.CASCADE)
    account_type = models.CharField(max_length=20,choices=ACCOUNT_TYPE)
    account_no = models.IntegerField(unique=True)
    gender = models.CharField(max_length=10, choices=GENDER_TYPE)
    initial_deposite_date = models.DateTimeField(auto_now_add=True)
    balance = models.DecimalField(default=0, max_digits=12, decimal_places=2)

    def __str__(self):
        return f"User_Acc_no: {self.account_no}"


class UserAddress(models.Model):
    user = models.OneToOneField(User, related_name='user_address', on_delete=models.CASCADE)
    birth_date = models.DateField(blank=True, null=True)
    street_address = models.CharField(max_length=100)
    city = models.CharField(max_length= 100)
    postal_code = models.IntegerField()
    country = models.CharField(max_length=100)
    def __str__(self):
        return f"User_Email: {self.user.email}"
    


    

