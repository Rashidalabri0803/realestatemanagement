from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BuildingViewSet,
    ExpenseViewSet,
    LeaseContractViewSet,
    MaintenanceRequestViewSet,
    NotifictionViewSet,
    PaymentViewSet,
    TenantViewSet,
    UnitViewSet,
)

router = DefaultRouter()
router.register('buildings', BuildingViewSet, basename='buildings')
router.register('units', UnitViewSet, basename='units')
router.register('tenants', TenantViewSet, basename='tenants')
router.register('contracts', LeaseContractViewSet, basename='leasecontract')
router.register('payments', PaymentViewSet, basename='payments')
router.register('maintenance', MaintenanceRequestViewSet, basename='maintenance')
router.register('expenses', ExpenseViewSet, basename='expenses')
router.register('notifications', NotifictionViewSet, basename='notifications')

urlpatterns = [
    path('api/', include(router.urls)),
]