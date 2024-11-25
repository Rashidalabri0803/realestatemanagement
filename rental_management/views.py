from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import status, viewsets
from rest_framework.decorators import action
from rest_framework.filters import OrderingFilter, SearchFilter
from rest_framework.response import Response

from .models import (
    Building,
    Expense,
    LeaseContract,
    MaintenanceRequest,
    Notifiction,
    Payment,
    Tenant,
    Unit,
)
from .serializers import (
    BuildingSerializer,
    ExpenseSerializer,
    LeaseContractSerializer,
    MaintenanceRequestSerializer,
    NotifictionSerializer,
    PaymentSerializer,
    TenantSerializer,
    UnitSerializer,
)


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

class UnitViewSet(viewsets.ModelViewSet):
    queryset = Unit.objects.select_related('building').all()
    serializer_class = UnitSerializer
    filter_backends = [DjangoFilterBackend]
    filterset_fields = ['building', 'unit_type', 'status']
    search_fields = ['number', 'building__name']
    ordering_fields = ['monthly_rent', 'area' , 'created_at']

    @action(detail=False, methods=['get'])
    def available_units(self, request):
        available_units = Unit.objects.filter(status='available')
        serializer = self.get_serializer(available_units, many=True, context={'request': request})
        return Response(serializer.data)

class TenantViewSet(viewsets.ModelViewSet):
    queryset = Tenant.objects.all()
    serializer_class = TenantSerializer
    filter_backends = [SearchFilter, OrderingFilter]
    filterset_fields = ['full_name', 'phone_number', 'email']
    ordering_fields = ['full_name']

    @action(detail=True, methods=['get'])
    def contracts(self, request, pk=None):
        tenant = get_object_or_404(Tenant, pk=pk)
        contracts = LeaseContract.objects.filter(tenant=tenant)
        serializer = LeaseContractSerializer(contracts, many=True, context={'request': request})
        return Response(serializer.data)

class LeaseContractViewSet(viewsets.ModelViewSet):
    queryset = LeaseContract.objects.select_related('unit', 'tenant').all()
    serializer_class = LeaseContractSerializer
    filter_backends = [DjangoFilterBackend, SearchFilter, OrderingFilter]
    filterset_fields = ['unit', 'tenant', 'is_active']
    search_fields = ['unit__number', 'tenant__full_name']
    ordering_fields = ['start_date', 'end_date']

    @action(detail=False, methods=['post'])
    def terminate_contract(self, request):
        contract_id = request.data.get('contract_id')
        contract = get_object_or_404(LeaseContract, pk=contract_id)
        contract.is_active = False
        contract.save()
        return Response({'message': f'تم إنهاء عقد الإيجار {contract_id} بنجاح.'}, status=status.HTTP_200_OK)

class PaymentViewSet(viewsets.ModelViewSet):
    queryset = Payment.objects.select_related('contract').all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['contract', 'payment_date']
    ordering_fields = ['payment_date' , 'amount']

class MaintenanceRequestViewSet(viewsets.ModelViewSet):
    queryset = MaintenanceRequest.objects.select_related('unit').all()
    serializer_class = MaintenanceRequestSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['unit', 'is_resolved']
    ordering_fields = ['request_date', 'resolved_date']

    @action(detail=False, methods=['get'])
    def unresolved(self, request):
        unresolved_requests = MaintenanceRequest.objects.filter(is_resolved=False)
        serializer = self.get_serializer(unresolved_requests, many=True, context={'request': request})
        return Response(serializer.data)

class ExpenseViewSet(viewsets.ModelViewSet):
    queryset = Expense.objects.select_related('building').all()
    serializer_class = ExpenseSerializer
    filter_backends = [DjangoFilterBackend, OrderingFilter]
    filterset_fields = ['building', 'date']
    ordering_fields = ['date', 'amount']

class NotifictionViewSet(viewsets.ModelViewSet):
    queryset = Notifiction.objects.all()
    serializer_class = NotifictionSerializer
    filter_backends = [OrderingFilter]
    ordering_fields = ['created_at']

    @action(detail=False, methods=['post'])
    def mark_as_read(self, request):
        Notifiction.objects.update(is_read=True)
        return Response({'message': 'تم تحديد جميع الإشعارات كمقروءة .'}, status=status.HTTP_200_OK)
        
