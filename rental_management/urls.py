from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (
    BuildingCreatView,
    BuildingDetaileView,
    BuildingListView,
    BuildingViewSet,
    InvoiceViewSet,
    LatePaymentViewSet,
    LeaseContractCreatView,
    LeaseContractViewSet,
    MainteanceRequestViewSet,
    MaintenanceFeedbackViewSet,
    MarkNotificationAsRead,
    NotificationViewSet,
    PaymentCretView,
    PaymentViewSet,
    ReminderViewSet,
    ReportViewSet,
    SystemReportViewSet,
    SystemSettingsViewSet,
    TenantViewSet,
    UnitCreateView,
    UnitDetaileView,
    UnitListView,
    UnitViewSet,
)

router = DefaultRouter()
router.register(r'buildings', BuildingViewSet, basename='buildings')
router.register(r'units', UnitViewSet, basename='units')
router.register(r'tenants', TenantViewSet, basename='tenants')
router.register(r'lease-contracts', LeaseContractViewSet, basename='lease-contracts')
router.register(r'invoices', InvoiceViewSet, basename='invoices')
router.register(r'payments', PaymentViewSet, basename='payments')
router.register(r'reminders', ReminderViewSet, basename='reminders')
router.register(r'notifications', NotificationViewSet, basename='notifications')
router.register(r'maintenance-requests', MainteanceRequestViewSet, basename='maintenance-requests')
router.register(r'maintenance-feedbacks', MaintenanceFeedbackViewSet, basename='maintenance-feedbacks')
router.register(r'late-payments', LatePaymentViewSet, basename='late-payments')
router.register(r'reports', ReportViewSet, basename='reports')
router.register(r'system-settings', SystemSettingsViewSet, basename='system-settings')


urlpatterns = [
    path('buildings/', BuildingListView.as_view(), name='building-list'),
    path('buildings/create/', BuildingCreatView.as_view(), name='building-create'),
    path('buildings/<int:pk>/', BuildingDetaileView.as_view(), name='building-detaile'),
    
    path('units/', UnitListView.as_view(), name='unit-list'),
    path('units/create/', UnitCreateView.as_view(), name='unit-create'),
    path('units/<int:pk>/', UnitDetaileView.as_view(), name='unit-detaile'),
    
    path('contracts/create/', LeaseContractCreatView.as_view(), name='contract-create'),

    path('payments/create/', PaymentCretView.as_view(), name='payment-create'),
    
    path('api/', include(router.urls)),

    path('api/notifictions/mark-as-read/', MarkNotificationAsRead.as_view({'post':'create'}), name='mark-notification-as-read'),
    path('api/system-report/', SystemReportViewSet.as_view({'get':'list'}), name='system-report'),
]
