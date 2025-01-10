from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from apps.expenses.models import ExpenseSplit
from apps.settlements.models import Settlement

User = get_user_model()


class SettlementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Settlement
        fields = ['id', 'expense_split', 'payer', 'payee', 'amount',
                  'payment_status', 'settlement_method', 'due_date']

    def validate_amount(self, value):
        """Ensure the settlement amount is valid."""
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero.")
        return value

    def validate(self, data):
        payer = data['payer']
        payee = data['payee']

        if payer == payee:
            raise serializers.ValidationError(
                "Payer and payee cannot be the same user.")
        return super().validate(data)

    def create(self, validated_data):
        with transaction.atomic():
            expense_split_id = validated_data.pop('expense_split')
            payer_id = validated_data.pop('payer')
            payee_id = validated_data.pop('payee')

            expense_split = ExpenseSplit.objects.get(pk=expense_split_id)
            payer = User.objects.get(pk=payer_id)
            payee = User.objects.get(pk=payee_id)

            settlement = Settlement.objects.create(
                expense_split=expense_split,
                payer=payer,
                payee=payee,
                **validated_data
            )

        return settlement
