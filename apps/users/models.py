from django.contrib.auth.models import AbstractUser
from django.db import models


from apps.users.managers import UserManager
from apps.utils.common_model import CommonModel


class User(AbstractUser, CommonModel):
    PAYMENT_METHOD_CHOICES = [
        ('UPI', 'UPI'),
        ('card', 'Credit/Debit Card'),
        ('cash', 'Cash'),
    ]
    username = None
    email = models.EmailField(unique=True, null=False, blank=False)
    first_name = models.CharField(max_length=30, blank=True, null=True)
    last_name = models.CharField(max_length=30, blank=True, null=True)
    college = models.CharField(max_length=255, null=True, blank=True)
    semester = models.IntegerField(null=True, blank=True)
    default_payment_methods = models.CharField(
        max_length=50,
        choices=PAYMENT_METHOD_CHOICES,
        default='UPI'
    )


    # add more field

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def __str__(self):
        return self.email