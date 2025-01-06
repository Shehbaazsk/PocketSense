from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Student(models.Model):
    class PaymentMethod(models.TextChoices):
        UPI = 'upi', 'UPI'
        CASH = 'cash', 'Cash'
        CARD = 'card', 'Credit/Debit Card'
    # One-to-one relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')

    college = models.CharField(max_length=100)
    semester = models.SmallIntegerField()
    default_payment_method = models.CharField(
        max_length=30,
        choices=PaymentMethod.choices,
        default=PaymentMethod.CASH,
    )

    def __str__(self):
        return f'{self.user.email} - {self.college}'