from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.response import Response

from .models import Building, Unit, Tenant, LeaseContract, Payment, MaintenanceRequest, Expense, Notifiction
from .serializers import BuildingSerializer, UnitSerializer, TenantSerializer, LeaseContractSerializer, PaymentSerializer, MaintenanceRequestSerializer, ExpenseSerializer, NotifictionSerializer

class BuildingViewSet(viewsets.ModelViewSet):
    queryset = Building.objects.all()
    serializer_class = BuildingSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['name', 'address']
    search_fields = ['name', 'address']
    ordering_fields = ['created_at', 'updated_at']

    @action(detail=True, methods=['get'])
    def units(self, request, pk=None):
        building = get_object_or_404(Building, pk=pk)
        units = building.unit_set.all()
        serializer = UnitSerializer(units, many=True, context={'request': request})
        return Response(serializer.data)

    @action(detail=False, methods=['get'])
    def statistics(self, request):
        total_buildings = Building.objects.count()
        total_units = Unit.objects.count()
        rented_units = Unit.objects.filter(status='rented').count()
        available_units = Unit.objects.filter(status='available').count()
        return Response({
            'total_buildings': total_buildings,
            'total_units': total_units,
            'rented_units': rented_units,
            'available_units': available_units,
        })