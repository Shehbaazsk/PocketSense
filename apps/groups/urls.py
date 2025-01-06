from django.urls import include, path
from rest_framework import routers

from apps.groups.apis.api_views import GroupViewSet

routers = routers.DefaultRouter()
routers.register(r'', GroupViewSet, basename='groups')

urlpatterns = [
    
]

urlpatterns += routers.urls