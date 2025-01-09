
from django.conf import settings
from django.db import models
from rest_framework import serializers

from apps.utils.middlewares import get_current_user


class CommonModel(models.Model):
    """Abstract base model with common fields"""

    id = models.AutoField(primary_key=True, editable=False)

    # INSTEAD OF EXPOSING PK WE CAN USE UUID
    # uuid = models.UUIDField(default=uuid4, unique=True)

    is_active = models.BooleanField(default=True)
    is_delete = models.BooleanField(default=False)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    created_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='created_%(class)s'
    )

    modified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL, null=True, related_name='modified_%(class)s'
    )

    class Meta:
        abstract = True

    def save(self, *args, **kwargs):
        current_user = get_current_user()
        if not self.pk:  # If the object is being created
            self.created_by = current_user if current_user and current_user.is_authenticated else None
        self.modified_by = current_user if current_user and current_user.is_authenticated else None
        super().save(*args, **kwargs)

    def delete(self, *args, **kwargs):
        self.is_delete = True
        self.save()

    def restore(self, *args, **kwargs):
        self.is_delete = False
        self.save()

    def activate_or_deactivate(self, *args, **kwargs):
        self.is_active = not self.is_active
        self.save()


class CommonModelSerializer(serializers.ModelSerializer):
    """Serializer for the CommonModel fields"""

    class Meta:
        # fields = ["uuid", "is_active", "is_delete", "created_at", "updated_at"]
        fields = ["id", "is_active", "is_delete", "created_at", "updated_at"]
