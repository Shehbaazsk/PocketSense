from django.shortcuts import get_object_or_404
from drf_yasg.utils import swagger_auto_schema
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.response import Response

from apps.expenses.models import Expense
from apps.expenses.serializers import ExpenseDetailSerializer, ExpenseSerializer
from apps.groups.models import Group


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_serializer_class(self):
        if self.action in ['retrieve', 'split_details']:
            return ExpenseDetailSerializer
        return ExpenseSerializer

    @swagger_auto_schema(
        request_body=ExpenseSerializer
    )
    def create(self, request, *args, **kwargs):
        return super().create(request, *args, **kwargs)

    def perform_create(self, serializer):
        group = get_object_or_404(Group, id=self.request.data.get('group'))
        serializer.save(created_by=self.request.user,
                        group=group, **self.request.data)

    def perform_destroy(self, instance):
        instance.is_delete = False
        instance.save()
