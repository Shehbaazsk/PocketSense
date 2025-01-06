from django.db import models
from django.contrib.auth import get_user_model

from apps.utils.common_model import CommonModel

User = get_user_model()
# Create your models here.
class Group(CommonModel,models.Model):
    
    class GroupType(models.TextChoices):
        HOSTEL_ROOMMATES = 'hostel_roommates', 'Hostel Roommates'
        PROJECT_TEAMS = 'project_teams', 'Project Teams'
        TRIP_GROUPS = 'trip_groups', 'Trip Groups'

    name = models.CharField(max_length=255)
    members = models.ManyToManyField(User, related_name="user_groups")
    group_type = models.CharField(
        max_length=50,
        choices=GroupType.choices,  
        default=GroupType.HOSTEL_ROOMMATES,  
    )
    def __str__(self):
        return self.name