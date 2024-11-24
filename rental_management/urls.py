from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BuildingViewSet,
    TenantViewSet,
    UnitViewSet,
    building_detail,
    building_list,
    tenant_list,
    unit_list,
)

router = DefaultRouter()
router.register('buildings', BuildingViewSet, basename='building')
router.register('units', UnitViewSet, basename='unit')
router.register('tenants', TenantViewSet, basename='tenant')

urlpatterns = [
    path('api/', include(router.urls)),
    path('buildings/', building_list, name='building_list'),
    path('units/', unit_list, name='unit_list'),
    path('tenants/', tenant_list, name='tenant_list'),
    path('buildings/<int:pk>/', building_detail, name='building_detail'),
]