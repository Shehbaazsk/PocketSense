from django.urls import path
from rest_framework.routers import DefaultRouter
from apps.accounts.students.apis.api_views import CreateStudentAPIView, StudentViewSet

router = DefaultRouter()
router.register(r'', StudentViewSet, basename='students')


urlpatterns = [
    path('', CreateStudentAPIView.as_view(), name='create-student'), 
]

urlpatterns += router.urls
