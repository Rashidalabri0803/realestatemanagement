from django.shortcuts import get_object_or_404, render
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import viewsets
from rest_framework.permissions import IsAuthenticated

from .models import Building, Invoice, LeaseContract, Tenant, Unit
from .serializers import (
    BuildingSerializer,
    InvoiceSerializer,
    LeaseContractSerializer,
    TenantSerializer,
    UnitSerializer,
)


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'address']
    permission_classes = [IsAuthenticated]

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['unit_type', 'status', 'building']
    permission_classes = [IsAuthenticated]

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['full_name', 'phone_number']
    permission_classes = [IsAuthenticated]

class LeaseContractViewSet(viewsets.ModelViewSet):
    queryset = LeaseContract.objects.all()
    serializer_class = LeaseContractSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['tenant', 'unit', 'is_active']
    permission_classes = [IsAuthenticated]

class InvoiceViewSet(viewsets.ModelViewSet):
    queryset = Invoice.objects.all()
    serializer_class = InvoiceSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['contract', 'is_paid']
    permission_classes = [IsAuthenticated]

def building_list(request):
    buildings = Building.objects.all()
    return render(request, 'rental_management/building_list.html', {'buildings': buildings})

def unit_list(request):
    units = Unit.objects.all()
    return render(request, 'rental_management/unit_list.html', {'units': units})

def tenant_list(request):
    tenants = Tenant.objects.all()
    return render(request, 'rental_management/tenant_list.html', {'tenants': tenants})

def building_detail(request, pk):
    building = get_object_or_404(Building, pk=pk)
    return render(request, 'rental_management/building_detail.html', {'building': building})