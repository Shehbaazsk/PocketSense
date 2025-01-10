from django.contrib.auth import get_user_model
from django.db import transaction
from rest_framework import serializers

from apps.expenses.models import Expense, ExpenseSplit

User = get_user_model()


class ExpenseSplitSerializer(serializers.ModelSerializer):
    class Meta:
        model = ExpenseSplit
        fields = ['user', 'amount', 'is_paid']


class SplitDetailSerializer(serializers.Serializer):
    user = serializers.StringRelatedField(read_only=True)


class ExpenseSerializer(serializers.ModelSerializer):
    split_details = serializers.JSONField(required=False, help_text="A dictionary mapping user IDs to their respective amounts or percentages. "
                                          "Example for 'percentage': {'1': 20, '3': 50, '4': 30}.")

    class Meta:
        model = Expense
        fields = ['id', 'group',  'amount', "description",
                  'category', 'split_type', 'date', "receipt_image", "split_details"]
        read_only_fields = ['id']

    def validate_amount(self, value):
        """Ensure the expense amount is greater than zero"""
        if value <= 0:
            raise serializers.ValidationError(
                "Amount must be greater than zero.")
        return value

    def create(self, validated_data):
        split_details = validated_data.pop("split_details")
        with transaction.atomic():
            expense = Expense.objects.create(**validated_data)

            self.split_expense(expense, split_details)

        return expense

    def split_expense(self, expense, split_details):
        users = expense.group.members.all()

        if expense.split_type == Expense.SplitType.EQUAL:
            equal_share = expense.amount / len(users)

            for user in users:
                ExpenseSplit.objects.create(
                    expense=expense,
                    user=user,
                    amount=equal_share
                )

        elif expense.split_type == Expense.SplitType.PERCENTAGE:
            total_percentage = sum(split_details.values())
            if total_percentage != 100:
                raise serializers.ValidationError(
                    "Total percentage must equal 100.")

            for user_id, percentage in split_details.items():
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    raise serializers.ValidationError(
                        f"User with ID {user_id} does not exist.")

                amount = (percentage / 100) * float(expense.amount)
                ExpenseSplit.objects.create(
                    expense=expense,
                    user=user,
                    amount=amount
                )

        elif expense.split_type == Expense.SplitType.EXACT:
            if sum(split_details.values()) != expense.amount:
                raise serializers.ValidationError(
                    "Total exact amounts must equal the expense amount.")

            for user_id, amount in split_details.items():
                try:
                    user = User.objects.get(id=user_id)
                except User.DoesNotExist:
                    raise serializers.ValidationError(
                        f"User with ID {user_id} does not exist.")

                ExpenseSplit.objects.create(
                    expense=expense,
                    user=user,
                    amount=amount
                )


class ExpenseDetailSerializer(serializers.ModelSerializer):
    split_details = ExpenseSplitSerializer(
        source='splits', many=True, read_only=True)
    receipt_image = serializers.ImageField()

    class Meta:
        model = Expense
        fields = [
            'id', 'group',  'amount', 'category', 'split_type',
            'date', 'description', 'split_details', 'receipt_image',
        ]
