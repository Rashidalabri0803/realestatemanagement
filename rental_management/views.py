from django.shortcuts import render, get_object_or_404, redirect
from django.urls import reverse
from django.contrib import messages
from django.views.generic import ListView, DetailView, CreateView, UpdateView, DeleteView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets, filters, status
from rest_framework.response import Response

from .models import Building, Unit, Tenant, LeaseContract, Invoice, Payment, Reminder, Notification, MaintenanceRequest, SystemSettings, MaintenanceFeedback, LatePayment, Report
from .forms import BuildingForm, UnitForm, TenantForm, LeaseContractForm, InvoiceForm, PaymentForm, ReminderForm, NotificationForm, MaintenanceRequestForm
from .serializers import BuildingSerializer, UnitSerializer, TenantSerializer, LeaseContractSerializer, InvoiceSerializer, PaymentSerializer, ReminderSerializer, NotificationSerializer, MaintenanceRequestSerializer, MaintenanceFeedbackSerializer, LatePaymentSerializer, ReportSerializer, SystemSettingsSerializer

class BuildingListView(ListView):
    model = Building
    template_name = 'buildings/building_list.html'
    context_object_name = 'buildings'
    
    def get_queryset(self):
        return Building.objects.filter(is_deleted=False).order_by("name")

class BuildingCreatView(CreateView):
    model = Building
    fields = ['name', 'address', 'description', 'image']
    template_name = 'buildings/building_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "تم إضافة المبنى بنجاح")
        return super().form_valid(form)

class BuildingDetaileView(DetailView):
    model = Building
    template_name = 'buildings/building_detail.html'
    context_object_name = 'building'

    def get_queryset(self):
        return Building.objects.filter(is_deleted=False)

class UnitListView(ListView):
    model = Unit
    template_name = 'units/unit_list.html'
    context_object_name = 'units'

    def get_queryset(self):
        return Unit.objects.filter(is_deleted=False).select_related('building')

class UnitCreateView(CreateView):
    model = Unit
    form_class = UnitForm
    template_name = 'units/unit_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "تم إضافة الوحدة بنجاح")
        return super().form_valid(form)

class UnitDetaileView(DetailView):
    model = Unit
    template_name = 'units/unit_detail.html'
    context_object_name = 'unit'

    def get_queryset(self):
        return Unit.objects.filter(is_deleted=False).select_related('building')

class LeaseContractCreatView(CreateView):
    model = LeaseContract
    form_class = LeaseContractForm
    template_name = 'contracts/contract_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "تم إضافة العقد بنجاح")
        return super().form_valid(form)

class PaymentCretView(CreateView):
    model = Payment
    form_class = PaymentForm
    template_name = 'payments/payment_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "تم إضافة الدفع بنجاح")
        return super().form_valid(form)

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.filter(is_deleted=False).prefetch_related('units')
    serializer_class = BuildingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'address']
    filterset_fields = ['created_at']

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.filter(is_deleted=False).prefetch_related('building')
    serializer_class = UnitSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['number', 'building__name']
    filterset_fields = ['unit_type', 'status']

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.filter(is_deleted=False)
    serializer_class = TenantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['full_name', 'phone_number']
    filterset_fields = ['created_at']

class LeaseContractViewSet(viewsets.ModelViewSet):
    queryset = LeaseContract.objects.filter(is_deleted=False).select_related('unit', 'tenant')
    serializer_class = LeaseContractSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['unit__building__name', 'unit__number']
    filterset_fields = ['start_date', 'end_date', 'is_active']

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.filter(is_deleted=False).select_related('contract', 'contract__unit', 'contract__tenant')
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['contract__tenant__full_name', 'contract__unit__number']
    filterset_fields = ['is_paid', 'due_date']

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.filter(is_deleted=False).select_related('contract')
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['contract__tenant__full_name']
    filterset_fields = ['payment_date']

class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.filter(is_deleted=False).select_related('tenant', 'contract')
    serializer_class = ReminderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['tenant__full_name', 'message']
    filterset_fields = ['is_sent']

class MainteanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.filter(is_deleted=False).select_related('unit')
    serializer_class = MaintenanceRequestSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['unit__number', 'descripton']
    filterset_fields = ['priority', 'is_resolved']

class NotificationViewSet(viewsets.ModelViewSet):
    queryset = Notification.objects.filter(is_deleted=False)
    serializer_class = NotificationSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['message']
    filterset_fields = ['is_read', 'priority']

class MaintenanceFeedbackViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceFeedback.objects.filter(is_deleted=False)
    serializer_class = MaintenanceFeedbackSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['maintenance_requests__unit__number', 'comments']
    filterset_fields = ['rating']

class LatePaymentViewSet(viewsets.ModelViewSet):
    queryset = LatePayment.objects.filter(is_deleted=False).select_related('invoice', 'invoice__contract')
    serializer_class = LatePaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['invoice__contract__tenant__full_name', 'invoice__contract__unit__number']
    filterset_fields = ['days_late']

class ReportViewSet(viewsets.ModelViewSet):
    queryset = Report.objects.filter(is_deleted=False)
    serializer_class = ReportSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'report_type']
    filterset_fields = ['generated_at']

class SystemSettingsViewSet(viewsets.ModelViewSet):
    queryset = SystemSettings.objects.filter(is_deleted=False)
    serializer_class = SystemSettingsSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['key', 'value']
    filterset_fields = ['created_at']

class MarkNotificationAsRead(viewsets.ViewSet):
    def create(self, request, *args, **kwargs):
        Notification.objects.filter(is_read=False).update(is_read=True)
        return Response({"message": "تم تحديد جميع الإشعارات كمقروءة"}, status=status.HTTP_200_OK)
        
class SystemReportViewSet(viewsets.ModelViewSet):
    def list(self, request, *args, **kwargs):
        total_buildings = Building.objects.filter(is_deleted=False).count()
        total_units = Unit.objects.filter(is_deleted=False).count()
        total_rent = sum(invoice.amount for invoice in Invoice.objects.filter(is_paid=True))
        total_tenants = Tenant.objects.filter(is_deleted=False).count()

        report = {
            "total_buildings": total_buildings,
            "total_units": total_units,
            "total_rent": total_rent,
            "total_tenants": total_tenants,
        }
        return Response(report, status=status.HTTP_200_OK)