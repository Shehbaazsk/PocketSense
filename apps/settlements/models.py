from django.contrib.auth import get_user_model
from django.db import models

from apps.expenses.models import ExpenseSplit
from apps.utils.common_model import CommonModel

User = get_user_model()

# Create your models here.


class Settlement(CommonModel, models.Model):

    class PaymentStatus(models.TextChoices):
        PENDING = 'pending', 'Pending'
        PAID = 'paid', 'Paid'

    class SettlementMethod(models.TextChoices):
        BANK_TRANSFER = 'bank_transfer', 'Bank Transfer'
        CASH = 'cash', 'Cash'
        UPI = 'upi', 'UPI'

    expense_split = models.ForeignKey(
        ExpenseSplit, on_delete=models.CASCADE, related_name='settlements')
    payer = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='debts')
    payee = models.ForeignKey(
        User, on_delete=models.CASCADE, related_name='credits')
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    payment_status = models.CharField(
        max_length=20, choices=PaymentStatus.choices, default=PaymentStatus.PENDING)
    settlement_method = models.CharField(
        max_length=20, choices=SettlementMethod.choices, default=SettlementMethod.CASH)
    due_date = models.DateField()
