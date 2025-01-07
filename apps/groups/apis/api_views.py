from rest_framework import viewsets
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated,IsAdminUser
from apps.groups.models import Group
from apps.groups.serializers import CreateUpdateGroupSerializer, GroupSerializer, RemoveMemberSerializer
from apps.utils.permissions import IsAdminOrOwner
from django.contrib.auth import get_user_model
from rest_framework.response import Response
from rest_framework import status


User = get_user_model()


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
        return super().get_serializer_class()
    
    def destroy(self, request, *args, **kwargs):
        """
        Override destroy to implement soft delete.
        """
        group = self.get_object()
        group.soft_delete()
        return Response({"detail": "Group has been soft deleted."}, status=status.HTTP_204_NO_CONTENT)
    
    @action(detail=True, url_path="leave-group",methods=['get'], permission_classes=[IsAuthenticated])
    def leave_group(self, request, pk=None):
        """
        Allow the authenticated user to leave the group.
        """
        group = self.get_object()
        if request.user in group.members.all():
            group.members.remove(request.user)
            return Response({"detail": "You have left the group."}, status=status.HTTP_200_OK)
        return Response({"detail": "You are not a member of this group."}, status=status.HTTP_400_BAD_REQUEST)
    
    @action(detail=True, url_path='remove-members',methods=['post'], permission_classes=[IsAdminUser],serializer_class=RemoveMemberSerializer)
    def remove_members(self, request, pk=None):
        """
        Remove a specific member from the group.
        """
        serializer = RemoveMemberSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        member_ids = serializer.validated_data['member_ids']
        group = self.get_object()
        members_in_group = group.members.filter(id__in=member_ids)

        if not members_in_group.exists():
            return Response(
                {"detail": "No valid members to remove from the group."},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        group.members.remove(*members_in_group)

        return Response({
            "detail": "Members removed successfully."
        },status=status.HTTP_200_OK)
    
    @action(detail=True, methods=['get'],url_path='activate-or-deactivate')
    def active_or_deactivate(self, request, pk=None):
        """
        Activate or deactivate a group 
        """
        group = self.get_object()
        group.activate_or_deactivate()
        action = "activated" if group.is_active else "deactivated"
        return Response({"detail": f"Group has been {action}."}, status=status.HTTP_200_OK)
