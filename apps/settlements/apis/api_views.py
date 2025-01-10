from rest_framework import viewsets

from apps.settlements.models import Settlement
from apps.settlements.serializers import SettlementSerializer


class SettlementViewSet(viewsets.ModelViewSet):
    queryset = Settlement.objects.all()
    serializer_class = SettlementSerializer
