from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BuildingViewSet,
    ExpenseViewSet,
    MaintenceRequestViewSet,
    RentReportViewSet,
    TenantBankAccountViewSet,
    TenantViewSet,
    UnitViewSet,
)

router = DefaultRouter()
router.register('buildings', BuildingViewSet, basename='building')
router.register('units', UnitViewSet, basename='unit')
router.register('tenants', TenantViewSet, basename='tenant')
router.register('maintenance', MaintenceRequestViewSet, basename='maintenance')
router.register('expenses', ExpenseViewSet, basename='expense')
router.register('bank-accounts', TenantBankAccountViewSet, basename='bankaccount')
router.register('rent-reports', RentReportViewSet, basename='rentreport')

urlpatterns = [
    path('api/', include(router.urls)),
    path('api/buildings/<int:pk>/units/', BuildingViewSet.as_view({'get': 'units'}), name='building-units'),
    path('api/buildings/statistic/', BuildingViewSet.as_view({'get': 'statistics'}), name='building-statistics'),
    path('api/units/available/', UnitViewSet.as_view({'get': 'available_units'}), name='available_units'),
    path('api/maintenance/unresolved/', MaintenceRequestViewSet.as_view({'get': 'unresolved'}), name= 'unresolved-maintenance'),
    path('api/rent-reports/generated/', RentReportViewSet.as_view({'post': 'generated_report'}), name='generated-rent-report'),
]