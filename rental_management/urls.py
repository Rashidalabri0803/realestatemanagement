from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BuildingViewSet,
    InvoiceViewSet,
    LeaseContractViewSet,
    TenantViewSet,
    UnitViewSet,
)

router = DefaultRouter()
router.register('buildings', BuildingViewSet, basename='building')
router.register('units', UnitViewSet, basename='unit')
router.register('tenants', TenantViewSet, basename='tenant')
router.register('contracts', LeaseContractViewSet, basename='contract')
router.register('invoices', InvoiceViewSet, basename='invoice')

urlpatterns = [
    path('', include(router.urls)),
]