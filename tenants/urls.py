from rest_framework.routers import DefaultRouter
from .views import TenantViewSet

router = DefaultRouter()
router.register(r'tenants', TenantViewSet)

urlpattens = router.urls