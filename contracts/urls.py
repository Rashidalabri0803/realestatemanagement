from rest_framework.routers import DefaultRouter
from .views import LeasContractViewSet

router = DefaultRouter()
router.register(r'contracts', LeasContractViewSet)

urlpatterns = router.urls