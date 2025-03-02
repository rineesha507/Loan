from django.contrib.auth.models import AbstractUser
from django.db import models
import random
from django.contrib.auth import get_user_model
from datetime import timedelta, date


class CustomUser(AbstractUser):
    ROLE_CHOICES = (
        ('admin', 'Admin'),
        ('user', 'User'),
    )
    
    role = models.CharField(max_length=10, choices=ROLE_CHOICES, default='user')
    is_verified = models.BooleanField(default=False)  # Email Verification Status
    otp = models.CharField(max_length=6, blank=True, null=True)  # Store OTP

    def generate_otp(self):
        self.otp = str(random.randint(100000, 999999))  # Generate 6-digit OTP
        self.save()

    def __str__(self):
        return self.username
    
User = get_user_model()
    
class Loan(models.Model):
    loan_id = models.CharField(max_length=20, unique=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="loans")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    tenure = models.IntegerField()  # In months
    interest_rate = models.FloatField()  # Yearly interest rate
    monthly_installment = models.DecimalField(max_digits=10, decimal_places=2)
    total_interest = models.DecimalField(max_digits=10, decimal_places=2)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)
    amount_paid = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    amount_remaining = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=10, choices=[('ACTIVE', 'Active'), ('CLOSED', 'Closed')], default="ACTIVE")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.loan_id
    

class LoanPaymentSchedule(models.Model):
    loan = models.ForeignKey(Loan, on_delete=models.CASCADE, related_name="payment_schedule")
    installment_no = models.IntegerField()
    due_date = models.DateField()
    amount = models.DecimalField(max_digits=10, decimal_places=2)