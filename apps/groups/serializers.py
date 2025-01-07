
from rest_framework import serializers
from django.contrib.auth import get_user_model

from apps.accounts.users.serializers import UserSerializer
from apps.groups.models import Group

User = get_user_model()

class GroupSerializer(serializers.ModelSerializer):
    members = UserSerializer(many=True)

    class Meta:
        model = Group
        exclude = ["is_delete"]
    
class CreateUpdateGroupSerializer(serializers.ModelSerializer):
    class Meta:
        model = Group
        exclude = ["is_delete"]

class RemoveMemberSerializer(serializers.Serializer):
    member_id = serializers.ListField(
        child= serializers.IntegerField(),
        allow_empty=False,
        help_text="A list of member IDs to be removed from the group."
        )
