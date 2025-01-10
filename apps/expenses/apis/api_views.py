from rest_framework import status, viewsets
from rest_framework.parsers import FormParser, MultiPartParser
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.expenses.models import Expense
from apps.expenses.serializers import ExpenseDetailSerializer, ExpenseSerializer
from apps.utils.permissions import IsAdminOrOwner


class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    parser_classes = (MultiPartParser, FormParser)

    def get_permissions(self):
        if self.action == 'delete':
            return [IsAdminUser()]
        elif self.action in ('update', 'list', 'retrieve'):
            return [IsAdminOrOwner()]
        return super().get_permissions()

    def get_serializer_class(self):
        if self.action in ['list', 'retrieve']:
            return ExpenseDetailSerializer
        return ExpenseSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def perform_destroy(self, instance):
        instance.is_delete = False
        instance.save()
