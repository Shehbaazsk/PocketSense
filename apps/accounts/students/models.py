from django.db import models
from django.contrib.auth import get_user_model
# Create your models here.

User = get_user_model()

class Student(models.Model):
    PAYMENT_METHOD_CHOICES = [
        ('upi', 'UPI'),
        ('cash', 'Cash'),
        ('card', 'Credit/Debit Card'),
    ]

    # One-to-one relationship with the User model
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')

    college = models.CharField(max_length=100)
    semester = models.SmallIntegerField()
    default_payment_method = models.CharField(
        max_length=30,
        choices=PAYMENT_METHOD_CHOICES,
        default='cash',
    )

    def __str__(self):
        return f'{self.user.email} - {self.college}'