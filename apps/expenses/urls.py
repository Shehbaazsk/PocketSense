from rest_framework import routers

from apps.expenses.apis.api_views import ExpenseViewSet

routers = routers.DefaultRouter()
routers.register(r'', ExpenseViewSet, basename='expenses')

urlpatterns = [

]

urlpatterns += routers.urls
