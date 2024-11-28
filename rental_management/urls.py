from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BuildingCreateView,
    BuildingDeleteView,
    BuildingDetailView,
    BuildingListView,
    BuildingUpdateView,
    BuildingViewSet,
    ExpenseCreateView,
    ExpenseDeleteView,
    ExpenseListView,
    ExpenseUpdateView,
    ExpenseViewSet,
    LeaseContractCreateView,
    LeaseContractDeleteView,
    LeaseContractListView,
    LeaseContractUpdateView,
    LeaseContractViewSet,
    MaintenanceRequestViewSet,
    MaitenanceRequestCreateView,
    MaitenanceRequestDeleteView,
    MaitenanceRequestListView,
    MaitenanceRequestUpdateView,
    NotifictionListView,
    NotifictionViewSet,
    PaymentViewSet,
    TenantCreateView,
    TenantDeleteView,
    TenantListView,
    TenantUpdateView,
    TenantViewSet,
    UnitCreateView,
    UnitDeleteView,
    UnitListView,
    UnitUpdateView,
    UnitViewSet,
)

router = DefaultRouter()
router.register(r'buildings', BuildingViewSet, basename='buildings')
router.register(r'units', UnitViewSet, basename='units')
router.register(r'tenants', TenantViewSet, basename='tenants')
router.register(r'contracts', LeaseContractViewSet, basename='leasecontract')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'maintenance', MaintenanceRequestViewSet, basename='maintenance')
router.register(r'expenses', ExpenseViewSet, basename='expenses')
router.register(r'notifications', NotifictionViewSet, basename='notifications')

urlpatterns = [
    path('api/', include(router.urls)),
    
    path('buildings/', BuildingListView.as_view(), name='building_list'),
    path('buildings/create/', BuildingCreateView.as_view(), name='building_create'),
    path('buildings/<int:pk>/', BuildingDetailView.as_view(), name='building_detail'),
    path('buildings/<int:pk>/edit/', BuildingUpdateView.as_view(), name='building_edit'),
    path('buildings/<int:pk>/delete/', BuildingDeleteView.as_view(), name='building_delete'),

    path('units/', UnitListView.as_view(), name='unit_list'),
    path('units/create/', UnitCreateView.as_view(), name='unit_create'),
    path('units/<int:pk>/edit/', UnitUpdateView.as_view(), name='unit_edit'),
    path('units/<int:pk>/delete/', UnitDeleteView.as_view(), name='unit_delete'),

    path('tenants/', TenantListView.as_view(), name='tenant_list'),
    path('tenants/create/', TenantCreateView.as_view(), name='tenant_create'),
    path('tenants/<int:pk>/edit/', TenantUpdateView.as_view(), name='tenant_edit'),
    path('tenants/<int:pk>/delete/', TenantDeleteView.as_view(), name='tenant_delete'),

    path('contracts/', LeaseContractListView.as_view(), name='leasecontract_list'),
    path('contracts/create/', LeaseContractCreateView.as_view(), name='leasecontract_create'),
    path('contracts/<int:pk>/edit/', LeaseContractUpdateView.as_view(), name='leasecontract_edit'),
    path('contracts/<int:pk>/delete/', LeaseContractDeleteView.as_view(), name='leasecontract_delete'),

    path('maintenance/', MaitenanceRequestListView.as_view(), name='maintenance_request_list'),
    path('maintenance/create/', MaitenanceRequestCreateView.as_view(), name='maintenance_request_create'),
    path('maintenance/<int:pk>/edit/', MaitenanceRequestUpdateView.as_view(), name='maintenance_request_edit'),
    path('maintenance/<int:pk>/delete/', MaitenanceRequestDeleteView.as_view(), name='maintenance_request_delete'),

    path('expenses/', ExpenseListView.as_view(), name='expense_list'),
    
    path('expenses/create/', ExpenseCreateView.as_view(), name='expense_create'),
    path('expenses/<int:pk>/edit/', ExpenseUpdateView.as_view(), name='expense_edit'),
    path('expenses/<int:pk>/delete/', ExpenseDeleteView.as_view(), name='expense_delete'),

    path('notifications/', NotifictionListView.as_view(), name='notification_list'),

    path('docs/', include('rest_framework.urls')),
]