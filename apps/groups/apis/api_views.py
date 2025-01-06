from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated
from apps.groups.models import Group
from apps.groups.serializers import CreateUpdateGroupSerializer, GroupSerializer
from apps.utils.permissions import IsAdminOrOwner


class GroupViewSet(viewsets.ModelViewSet):
    queryset = Group.objects.all()
    serializer_class = GroupSerializer
    permission_classes = [IsAuthenticated, IsAdminOrOwner]
    
    def get_queryset(self):
        """
        Restrict queryset to the authenticated user unless the user is admin.
        """
        if self.request.user.is_superuser:
            return super().get_queryset()
        return super().get_queryset().filter(members=self.request.user)

    def get_serializer_class(self):
        if self.action in ['create', 'update','partial_update']:
            return CreateUpdateGroupSerializer
        return super.get_serializer_class()