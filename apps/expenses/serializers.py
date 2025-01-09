from rest_framework import serializers

from .models import Expense


class ExpenseSerializer(serializers.ModelSerializer):

    class Meta:
        model = Expense
        fields = ['group',  'amount', "description",
                  'category', 'split_type', 'date', "receipt_image"]

    def validate(self, data):
        """
        Additional validation to ensure valid inputs for split types.
        """
        if data['split_type'] == 'percentage' and 'split_details' not in self.context:
            raise serializers.ValidationError(
                "Percentage split requires split details.")
        if data['split_type'] == 'exact' and 'split_details' not in self.context:
            raise serializers.ValidationError(
                "Exact split requires split details.")
        return data


class ExpenseDetailSerializer(serializers.ModelSerializer):
    split_details = serializers.SerializerMethodField()
    receipt_image = serializers.ImageField()

    class Meta:
        model = Expense
        fields = [
            'id', 'group',  'amount', 'category', 'split_type',
            'date', 'description', 'split_details', 'receipt_image'
        ]

    def get_split_details(self, obj):
        """
        Calculate split details for the expense.
        """
        return obj.calculate_split()
