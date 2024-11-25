from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BuildingViewSet,
    ExpenseViewSet,
    MaintenanceRequestViewSet,
    TenantViewSet,
    UnitViewSet,
)

router = DefaultRouter()
router.register(r'buildings', BuildingViewSet, basename='building')
router.register(r'units', UnitViewSet, basename='unit')
router.register(r'tenants', TenantViewSet, basename='tenant')
router.register(r'maintenance_requests', MaintenanceRequestViewSet, basename='maintenance_request')
router.register(r'expenses', ExpenseViewSet, basename='expense')



urlpatterns = [
    path('api/', include(router.urls)),

    path('api/buildings/<int:pk>/units/', BuildingViewSet.as_view({'get': 'units'}), name='building-units'),
    path('api/buildings/statistics/', BuildingViewSet.as_view({'get': 'statistics'}), name='building-statistics'),
    path('api/units/available/', UnitViewSet.as_view({'get': 'available_units'}), name='available-units'),
  path('api/maintenance/unresolved/', MaintenanceRequestViewSet.as_view({'get': 'unresolved'}), name= 'unresolved-maintenance'),
]