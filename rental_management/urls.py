from django.urls import include, path
from rest_framework.routers import DefaultRouter

from . import views
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
    path('buildings/', views.BuildingListView.as_view(), name='buildings'),
    path('buildings/create/', views.BuildingCreateView.as_view(), name='building_create'),
    path('buildings/<int:pk>/', views.BuildingDetailView.as_view(), name='building_detail'),
    path('buildings/<int:pk>/edit/', views.BuildingUpdateView.as_view(), name='building_edit'),
    path('buildings/<int:pk>/delete/', views.BuildingDeleteView.as_view(), name='building_delete'),

    path('units/', views.UnitListView.as_view(), name='units'),
    path('units/create/', views.UnitCreateView.as_view(), name='unit_create'),
    path('units/<int:pk>/edit/', views.UnitUpdateView.as_view(), name='unit_edit'),
    path('units/<int:pk>/delete/', views.UnitDeleteView.as_view(), name='unit_delete'),

    path('tenants/', views.TenantListView.as_view(), name='tenants'),
    path('tenants/create/', views.TenantCreateView.as_view(), name='tenant_create'),
    path('tenants/<int:pk>/edit/', views.TenantUpdateView.as_view(), name='tenant_edit'),
    path('tenants/<int:pk>/delete/', views.TenantDeleteView.as_view(), name='tenant_delete'),

    path('docs/', include('rest_framework.urls')),
]