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

