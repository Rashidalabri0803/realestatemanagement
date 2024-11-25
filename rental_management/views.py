from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import (
    Building,
    Expense,
    MaintenanceRequest,
    RentReport,
    Tenant,
    TenantBankAccount,
    Unit,
)
from .serializers import (
    BuildingSerializer,
    ExpenseSerializer,
    MaintenanceRequestSerializer,
    TenantSerializer,
    UnitSerializer,
)


class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'address']

    @action(detail=True, methods=['get']) 
    def units(self, request, pk=None):
        building = get_object_or_404(Building, pk=pk)
        units = building.unit_set.all()
        serializer = UnitSerializer(units, many=True)
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total_buildings = Building.objects.count()
        total_units = Unit.objects.count()
        available_units = Unit.objects.filter(status='Available').count()
        return Response({
            'total_buildings': total_buildings, 
            'total_units': total_units, 
            'available_units': available_units,
        })

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.all()
    serializer_class = UnitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['building', 'unit_type', 'status']

    @action(detail=False, methods=['get']) 
    def available_units(self, request):
        available_units = Unit.objects.filter(status='Available')
        serializer = self.get_serializer(available_units, many=True)
        return Response(serializer.data)

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['full_name', 'phone_number', 'email']

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.all()
    serializer_class = MaintenanceRequestSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['unit', 'is_resolved']

    @action(detail=False, methods=['get']) 
    def unresolved(self, request):
        unresolved_requests = MaintenanceRequest.objects.filter(is_resolved=False)
        serializer = self.get_serializer(unresolved_requests, many=True)
        return Response(serializer.data)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['building', 'date']

        building = get_object_or_404(Building, pk=building_id)
        report = RentReport.objects.create(building=building, total_income=total_income)
        serializer = self.get_serializer(report)
        return Response(serializer.data, status=status.HTTP_201_CREATED)