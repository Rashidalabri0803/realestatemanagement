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
router.register('buildings', BuildingViewSet)
router.register('units', UnitViewSet)
router.register('tenants', TenantViewSet)
router.register('lease-contracts', LeaseContractViewSet)
router.register('invoices', InvoiceViewSet)
router.register('payments', PaymentViewSet)
router.register('reminders', ReminderViewSet)
router.register('notifications', NotificationViewSet)
router.register('maintenance-requests', MainteanceRequestViewSet)
router.register('maintenance-feedbacks', MaintenanceFeedbackViewSet)
router.register('late-payments', LatePaymentViewSet)
router.register('reports', ReportViewSet)
router.register('system-settings', SystemSettingsViewSet)


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
