from rest_framework.routers import DefaultRouter

from apps.settlements.apis.api_views import SettlementViewSet

router = DefaultRouter()
router.register(r'settlements', SettlementViewSet, basename='settlements')

urlpatterns = [
]

urlpatterns += router.urls
