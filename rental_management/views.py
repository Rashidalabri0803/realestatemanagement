from django.contrib import messages
from django.views.generic import CreateView, ListView
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters, viewsets

from .forms import LeaseContractForm, UnitForm
from .models import Building, Invoice, LeaseContract, Reminder, Tenant, Unit
from .serializers import (
    BuildingSerializer,
    InvoiceSerializer,
    LeaseContractSerializer,
    ReminderSerializer,
    TenantSerializer,
    UnitSerializer,
)


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

class LeaseContractCreatView(CreateView):
    model = LeaseContract
    form_class = LeaseContractForm
    template_name = 'contracts/contract_form.html'

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        messages.success(self.request, "تم إضافة العقد بنجاح")
        return super().form_valid(form)

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.filter(is_deleted=False).prefetch_related('units')
    serializer_class = BuildingSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['name', 'address']
    filterset_fields = ['crearted_at']

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.filter(is_deleted=False).select_related('building')
    serializer_class = UnitSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['building__name', 'number']
    filterset_fields = ['unit_type', 'status']

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.filter(is_deleted=False)
    serializer_class = TenantSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['full_name', 'phone_number']
    filterset_fields = ['created_at']

class LeaseContractViewSet(viewsets.ModelViewSet):
    queryset = LeaseContract.objects.filter(is_deleted=False).select_related('tenant', 'unit')
    serializer_class = LeaseContractSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['tenant__full_name', 'unit__number']
    filterset_fields = ['start_date', 'end_date', 'is_active']

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.filter(is_deleted=False).select_related('contract', 'contract__unit', 'contract__tenant')
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['contract__tenant__full_name', 'contract__unit__number']
    filterset_fields = ['is_paid', 'due_date']

class ReminderViewSet(viewsets.ModelViewSet):
    queryset = Reminder.objects.filter(is_deleted=False).select_related('tenant', 'contract')
    serializer_class = ReminderSerializer
    filter_backends = [DjangoFilterBackend, filters.SearchFilter]
    search_fields = ['tenant__full_name', 'message']
    filterset_fields = ['is_sent']