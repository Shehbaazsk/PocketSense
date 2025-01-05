from django.urls import path

from apps.accounts.students.apis.api_views import CreateStudentAPIView


urlpatterns = [
    path('', CreateStudentAPIView.as_view(), name='create-student'), 
]
