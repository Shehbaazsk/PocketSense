from django_filters import rest_framework as filters

from .models import Expense


class ExpenseFilter(filters.FilterSet):
    group_name = filters.CharFilter(
        field_name='group__name', lookup_expr='icontains')
    member_name = filters.CharFilter(
        field_name='group__members__first_name', lookup_expr='icontains')

    class Meta:
        model = Expense
        fields = ['category', 'split_type', 'group_name', 'member_name']
