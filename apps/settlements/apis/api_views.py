from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAdminUser
from rest_framework.response import Response

from apps.settlements.models import Settlement
from apps.settlements.serializers import SettlementSerializer
from apps.utils.permissions import IsAdminOrOwner


class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.filter(is_delete=False)
    serializer_class = SettlementSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    filterset_fields = ['payer', 'payee', 'payment_status',]
    search_fields = ['payer__first_name', 'payee__first_name', ]

    def get_permissions(self):
        if self.action == 'delete':
            return [IsAdminUser()]
        elif self.action in ('update', 'list', 'retrieve'):
            return [IsAdminOrOwner()]
        return super().get_permissions()

    def perform_destroy(self, instance):
        instance.is_delete = False
        instance.save()

    @action(detail=False, methods=['get'])
    def unsettled(self, request):
        unsettled_settlements = Settlement.objects.filter(
            payment_status=Settlement.PaymentStatus.PENDING)
        serializer = self.get_serializer(unsettled_settlements, many=True)
        return Response(serializer.data)
