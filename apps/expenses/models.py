from django.contrib.auth import get_user_model
from django.db import models

from apps.groups.models import Group
from apps.utils.common_model import CommonModel

# Create your models here.
User = get_user_model()


class Expense(CommonModel, models.Model):
    class SplitType(models.TextChoices):
        EQUAL = 'equal', 'Equal Split'
        PERCENTAGE = 'percentage', 'Percentage Split'
        EXACT = 'exact', 'Exact Amount Split'

    class CategoryType(models.TextChoices):
        FOOD = 'food', 'Food'
        TRAVEL = 'travel', 'Travel'
        ACADEMICS = 'academics', 'Academics'
        ENTERTAINMENT = 'entertainment', 'Entertainment'

    group = models.ForeignKey(
        Group, on_delete=models.CASCADE, related_name='expenses')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(
        max_length=20,
        choices=CategoryType.choices,
        default=CategoryType.FOOD
    )
    split_type = models.CharField(
        max_length=20,
        choices=SplitType.choices,
        default=SplitType.EQUAL
    )
    date = models.DateField()
    description = models.TextField(blank=True)
    receipt_image = models.ImageField(
        upload_to="receipts/", null=True, blank=True)

    def __str__(self):
        return f"{self.category} - {self.amount}"


class ExpenseSplit(models.Model):
    expense = models.ForeignKey(
        Expense, on_delete=models.CASCADE, related_name='splits')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(default=False)

    def __str__(self):
        return f"Split for {self.expense.id} by {self.user.username}"
